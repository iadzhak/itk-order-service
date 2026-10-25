from contextlib import asynccontextmanager

from tests.fixtures.in_memory_repositories import (
    InMemoryIdempotencyRepository,
    InMemoryInboxRepository,
    InMemoryOrderRepository,
    InMemoryOutboxRepository,
)


class InMemoryUnitOfWork:
    def __init__(self):
        self.orders = {}
        self.idempotency = {}
        self.outbox = {}
        self.inbox = {}
        self._committed = False

    @asynccontextmanager
    async def __call__(self):
        yield _InMemoryUoWImplementation(
            orders=self.orders,
            idempotency=self.idempotency,
            outbox=self.outbox,
            inbox=self.inbox,
        )
        self._committed = True


class _InMemoryUoWImplementation:
    def __init__(
        self, orders: dict, idempotency: dict, outbox: dict, inbox: dict
    ) -> None:
        self.orders = InMemoryOrderRepository(orders)
        self.idempotency = InMemoryIdempotencyRepository(idempotency)
        self.outbox = InMemoryOutboxRepository(outbox)
        self.inbox = InMemoryInboxRepository(inbox)

    async def commit(self):
        pass
