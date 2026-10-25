import json

from aiokafka import AIOKafkaConsumer

from app.application.ports.uow import UnitOfWorkPort
from app.infrastructure.logging import get_logger
from app.infrastructure.presistance.db import SessionLocal
from app.infrastructure.presistance.uow import UnitOfWork
from app.settings import conf

logger = get_logger(__name__)


class KafkaConsumer:
    def __init__(
        self, bootstrap_servers: str, topic: str, group_id: str, uow: UnitOfWorkPort
    ) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._topic = topic
        self._group_id = group_id
        self._uow = uow
        self._consumer: AIOKafkaConsumer | None = None

    async def start(self) -> None:
        self._consumer = AIOKafkaConsumer(
            self._topic,
            bootstrap_servers=self._bootstrap_servers,
            group_id=self._group_id,
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')) if v else None,
        )
        await self._consumer.start()

    async def run(self) -> None:
        await self.start()
        try:
            async for message in self._consumer:  # type: ignore[union-attr]
                if message.value is None:
                    continue

                event = message.value

                try:
                    async with self._uow() as uow:
                        await uow.inbox.create(
                            uow.inbox.CreateDTO(
                                event_id=f'{message.topic}:{message.partition}:{message.offset}',
                                event_type=event['event_type'],
                                payload=event,
                            )
                        )
                        await uow.commit()
                    await self._consumer.commit()  # type: ignore[union-attr]
                except Exception:
                    logger.exception('Ошибка обработки сообщения')
                    continue
        finally:
            await self._consumer.stop()  # type: ignore[union-attr]


def get_kafka_consumer():
    return KafkaConsumer(
        bootstrap_servers=conf.kafka_bootstrap_servers,
        topic=conf.topic_in,
        group_id=conf.group_id,
        uow=UnitOfWork(SessionLocal),
    )
