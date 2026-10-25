from app.application.ports.uow import UnitOfWorkPort
from app.application.usecases.order_cancelled import OrderCancelledUseCase
from app.application.usecases.order_shipped import OrderShippedUseCase
from app.domain.models import EventType
from app.infrastructure.logging import get_logger

logger = get_logger(__name__)


class ProcessInboxEvents:
    def __init__(
        self,
        uow: UnitOfWorkPort,
        order_shipped: OrderShippedUseCase,
        order_cancelled: OrderCancelledUseCase,
        batch_size: int = 10,
    ) -> None:
        self._uow = uow
        self._batch_size = batch_size
        self._order_shipped = order_shipped
        self._order_cancelled = order_cancelled

    async def __call__(self) -> None:
        async with self._uow() as uow:
            events = await uow.inbox.get_pending_events(self._batch_size)
            if not events:
                return

            for event in events:
                try:
                    if event.event_type == EventType.ORDER_SHIPPED:
                        await self._order_shipped(
                            self._order_shipped.EventDTO.model_validate(event.payload)
                        )
                    elif event.event_type == EventType.ORDER_CANCELLED:
                        await self._order_cancelled(
                            self._order_cancelled.EventDTO.model_validate(event.payload)
                        )
                    else:
                        logger.error(
                            f'Неизвестное событие {event.id}: {event.event_type}'
                        )
                        continue
                except Exception:
                    logger.exception(f'Ошибка обработики события {event.id}')
                    continue
                await uow.inbox.mark_as_processed(event.id)

            await uow.commit()
