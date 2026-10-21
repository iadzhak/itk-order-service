from tests.fixtures.in_memory_repositories import (
    InMemoryIdempotencyRepository,
    InMemoryOrderRepository,
)


class InMemoryUnitOfWork:
    def __init__(self):
        self.orders = {}
        self.idempotency = {}
        self._committed = False

    async def __aenter__(self):
        return _InMemoryUoWImplementation(
            orders=self.orders, idempotency=self.idempotency
        )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._committed = True


class _InMemoryUoWImplementation:
    def __init__(self, orders: dict, idempotency: dict):
        self.orders = InMemoryOrderRepository(orders)
        self.idempotency = InMemoryIdempotencyRepository(idempotency)

    async def commit(self):
        pass
