from app.application.ports.clients import CatalogServicePort
from app.application.ports.uow import UnitOfWorkPort
from app.application.ports.usecases import CreateOrderDTO
from app.domain.exceptions import IdempotencyError, ItemNotEnoughQuantity, ItemNotFound
from app.domain.models import Order


class CreateOrderUseCase:
    def __init__(self, uow: UnitOfWorkPort, catalog: CatalogServicePort) -> None:
        self._uow = uow
        self._catalog = catalog

    async def __call__(self, order: CreateOrderDTO) -> Order:

        async with self._uow() as uow:
            # check idempotency
            idempotency = await uow.idempotency.get_by_idempotency_key(
                order.idempotency_key
            )
            if idempotency:
                if idempotency.payload_hash == order.get_hash():
                    return Order.from_dict(idempotency.response)
                else:
                    raise IdempotencyError(order.idempotency_key)

        # check available_qty
        catalog_item = await self._catalog.get_item(order.item_id)
        if catalog_item is None:
            raise ItemNotFound(order.item_id)
        if catalog_item.available_qty < order.quantity:
            raise ItemNotEnoughQuantity(
                catalog_item.name, order.quantity, catalog_item.available_qty
            )

        async with self._uow() as uow:
            # create order
            db_order = await uow.orders.create(
                uow.orders.CreateDTO(
                    user_id=order.user_id,
                    quantity=order.quantity,
                    item_id=order.item_id,
                )
            )
            await uow.idempotency.create(
                uow.idempotency.CreateDTO(
                    idempotency_key=order.idempotency_key,
                    payload_hash=order.get_hash(),
                    response=db_order.to_dict(),
                )
            )
            await uow.commit()
        return db_order
