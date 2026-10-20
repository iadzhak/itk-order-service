from contextlib import AbstractAsyncContextManager
from typing import Protocol

from app.application.ports.repositories import IdempotencyRepository, OrderRepository


class UnitOfWorkImplementationPort(Protocol):
    async def commit(self) -> None: ...

    @property
    def orders(self) -> OrderRepository: ...

    @property
    def idempotency(self) -> IdempotencyRepository: ...


UnitOfWorkPort = AbstractAsyncContextManager[UnitOfWorkImplementationPort]
