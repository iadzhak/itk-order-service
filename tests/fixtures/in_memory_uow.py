from contextlib import asynccontextmanager

from tests.fixtures.in_memory_repositories import (
    InMemoryIdempotencyRepository,
    InMemoryOrderRepository,
    InMemoryOutboxRepository,
)


class InMemoryUnitOfWork:
    def __init__(self):
        self.orders = {}
        self.idempotency = {}
        self.outbox = {}
        self._committed = False

    @asynccontextmanager
    async def __call__(self):
        yield _InMemoryUoWImplementation(
            orders=self.orders, idempotency=self.idempotency, events=self.outbox
        )
        self._committed = True


class _InMemoryUoWImplementation:
    def __init__(self, orders: dict, idempotency: dict, events: dict) -> None:
        self.orders = InMemoryOrderRepository(orders)
        self.idempotency = InMemoryIdempotencyRepository(idempotency)
        self.outbox = InMemoryOutboxRepository(events)

    async def commit(self):
        pass
