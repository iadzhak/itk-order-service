from uuid import UUID

from pydantic import BaseModel

from app.application.ports.clients import NotificationServicePort
from app.application.ports.uow import UnitOfWorkPort
from app.domain.models import EventType


class OrderCancelledUseCase:
    class EventDTO(BaseModel):
        event_type: EventType
        order_id: UUID
        item_id: UUID
        quantity: int
        reason: str

    def __init__(self, uow: UnitOfWorkPort, notify: NotificationServicePort) -> None:
        self._uow = uow
        self._notify = notify

    async def __call__(self, event: EventDTO):
        async with self._uow() as uow:
            await uow.orders.mark_as_cancelled(event.order_id)
            await uow.commit()
        await self._notify.notify_cancelled(event.order_id, event.reason)
