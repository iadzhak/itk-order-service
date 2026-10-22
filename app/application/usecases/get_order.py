from uuid import UUID

from app.application.ports.uow import UnitOfWorkPort
from app.domain.exceptions import OrderNotFound
from app.domain.models import Order


class GetOrderUseCase:
    def __init__(self, uow: UnitOfWorkPort) -> None:
        self._uow = uow

    async def __call__(self, order_id: UUID) -> Order:
        async with self._uow() as uow:
            order = await uow.orders.get_by_id(order_id)
        if not order:
            raise OrderNotFound(order_id)
        return order
