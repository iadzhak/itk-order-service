import hashlib
from uuid import UUID

from pydantic import BaseModel, NonNegativeInt, PositiveInt

from app.application.ports.uow import UnitOfWorkPort
from app.domain.exceptions import IdempotencyError
from app.domain.models import Order


class CreateOrderDTO(BaseModel):
    user_id: NonNegativeInt
    quantity: PositiveInt
    item_id: UUID
    idempotency_key: UUID

    def get_hash(self) -> str:
        normalized_data = self.model_dump_json()
        data_bytes = normalized_data.encode('utf-8')
        hash_object = hashlib.sha256(data_bytes)
        return hash_object.hexdigest()


class CreateOrderUseCase:
    def __init__(self, uow: UnitOfWorkPort) -> None:
        self._uow = uow

    async def __call__(self, order: CreateOrderDTO) -> Order:

        async with self._uow as uow:
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

            # create order
            db_order = await uow.orders.create(
                uow.orders.CreateDTO(
                    user_id=order.user_id,
                    quantity=order.quantity,
                    item_id=order.item_id,
                    idempotency_key=order.idempotency_key,
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
