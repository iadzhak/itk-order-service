from uuid import UUID

from pydantic import BaseModel

from app.application.ports.uow import UnitOfWorkPort
from app.domain.models import EventType, Order, OrderStatus


class OrderCancelledUseCase:
    class EventDTO(BaseModel):
        event_type: EventType
        order_id: UUID
        item_id: UUID
        quantity: int
        reason: str

    def __init__(self, uow: UnitOfWorkPort) -> None:
        self._uow = uow

    async def __call__(self, event: EventDTO):
        async with self._uow() as uow:
            await uow.orders.mark_as_cancelled(event.order_id)
            await uow.outbox.create(
                uow.outbox.CreateDTO(
                    event_type=EventType.NOTIFICATION,
                    payload=Order.make_notification(
                        event.order_id, OrderStatus.CANCELLED, event.reason
                    ),
                )
            )
            await uow.commit()
