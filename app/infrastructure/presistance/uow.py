from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infrastructure.presistance.db import SessionLocal
from app.infrastructure.presistance.repositories import (
    SAIdempotencyRepository,
    SAInboxRepository,
    SAOrderRepository,
    SAOutboxRepository,
)


class UnitOfWork:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    @asynccontextmanager
    async def __call__(self):
        async with self._session_factory() as session:
            try:
                yield _UnitOfWorkImplementation(session)
                await session.rollback()
            except Exception:
                await session.rollback()
                raise


class _UnitOfWorkImplementation:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._orders = SAOrderRepository(session)
        self._idempotency = SAIdempotencyRepository(session)
        self._outbox = SAOutboxRepository(session)
        self._inbox = SAInboxRepository(session)

    @property
    def orders(self) -> SAOrderRepository:
        return self._orders

    @property
    def idempotency(self) -> SAIdempotencyRepository:
        return self._idempotency

    @property
    def outbox(self) -> SAOutboxRepository:
        return self._outbox

    @property
    def inbox(self) -> SAInboxRepository:
        return self._inbox

    async def commit(self):
        await self._session.commit()


def get_unit_of_work() -> UnitOfWork:
    return UnitOfWork(SessionLocal)
