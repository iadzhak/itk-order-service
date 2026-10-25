import asyncio

from app.application.usecases.process_outbox_events import ProcessOutboxEvents
from app.infrastructure.kafka_producer import KafkaProducer
from app.infrastructure.presistance.db import SessionLocal
from app.infrastructure.presistance.uow import UnitOfWork
from app.settings import conf


class OutboxWorker:
    def __init__(self, use_case: ProcessOutboxEvents) -> None:
        self._use_case = use_case

    async def run(self):
        while True:
            await self._use_case()
            await asyncio.sleep(0.1)


def create_outbox_worker() -> OutboxWorker:
    return OutboxWorker(
        ProcessOutboxEvents(
            uow=UnitOfWork(SessionLocal),
            kafka_producer=KafkaProducer(
                bootstrap_servers=conf.kafka_bootstrap_servers, topic=conf.topic_out
            ),
        )
    )
