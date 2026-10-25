from app.application.ports.clients import NotificationServicePort
from app.application.ports.uow import UnitOfWorkPort
from app.domain.models import EventType
from app.infrastructure.kafka_producer import KafkaProducer
from app.infrastructure.logging import get_logger

logger = get_logger(__name__)


class ProcessOutboxEvents:
    def __init__(
        self,
        uow: UnitOfWorkPort,
        kafka_producer: KafkaProducer,
        notification_service: NotificationServicePort,
        batch_size: int = 10,
    ) -> None:
        self._uow = uow
        self._kp = kafka_producer
        self.notify = notification_service
        self._batch_size = batch_size

    async def __call__(self) -> None:
        async with self._uow() as uow:
            events = await uow.outbox.get_pending_for_update(limit=self._batch_size)
            if not events:
                return

            async with self._kp as kp:
                for event in events:
                    try:
                        if event.event_type == EventType.NOTIFICATION:
                            await self.notify.notify(
                                self.notify.NotificationDTO.model_validate(
                                    event.payload
                                )
                            )
                        else:
                            await kp.send_message(
                                message={
                                    'event_type': event.event_type,
                                    **event.payload,
                                },
                                key=event.payload.get('order_id'),
                            )
                    except Exception:
                        logger.exception('Не удалосб отправить сообщение %s', event.id)
                        continue
                    await uow.outbox.mark_as_sent(event.id)
                await uow.commit()
