from contextlib import asynccontextmanager

from tests.fixtures.in_memory_repositories import (
    InMemoryIdempotencyRepository,
    InMemoryOrderRepository,
)


class InMemoryUnitOfWork:
    def __init__(self):
        self.orders = {}
        self.idempotency = {}
        self._committed = False

    @asynccontextmanager
    async def __call__(self):
        yield _InMemoryUoWImplementation(
            orders=self.orders, idempotency=self.idempotency
        )
        self._committed = True


class _InMemoryUoWImplementation:
    def __init__(self, orders: dict, idempotency: dict):
        self.orders = InMemoryOrderRepository(orders)
        self.idempotency = InMemoryIdempotencyRepository(idempotency)

    async def commit(self):
        pass
