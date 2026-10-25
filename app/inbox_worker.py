import asyncio

from app.application.usecases.order_cancelled import OrderCancelledUseCase
from app.application.usecases.order_shipped import OrderShippedUseCase
from app.application.usecases.process_inbox_events import ProcessInboxEvents
from app.infrastructure.presistance.db import SessionLocal
from app.infrastructure.presistance.uow import UnitOfWork


class InboxWorker:
    def __init__(self, use_case: ProcessInboxEvents) -> None:
        self._use_case = use_case

    async def run(self) -> None:
        while True:
            await self._use_case()
            await asyncio.sleep(0.1)


def get_inbox_worker() -> InboxWorker:
    return InboxWorker(
        ProcessInboxEvents(
            uow=UnitOfWork(SessionLocal),
            order_shipped=OrderShippedUseCase(UnitOfWork(SessionLocal)),
            order_cancelled=OrderCancelledUseCase(UnitOfWork(SessionLocal)),
        )
    )
