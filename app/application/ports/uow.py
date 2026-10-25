from contextlib import AbstractAsyncContextManager
from typing import Protocol

from app.application.ports.repositories import (
    IdempotencyRepository,
    InboxRepository,
    OrderRepository,
    OutboxRepository,
)


class UnitOfWorkImplementationPort(Protocol):
    async def commit(self) -> None: ...

    @property
    def orders(self) -> OrderRepository: ...

    @property
    def idempotency(self) -> IdempotencyRepository: ...

    @property
    def outbox(self) -> OutboxRepository: ...

    @property
    def inbox(self) -> InboxRepository: ...


class UnitOfWorkPort(Protocol):
    def __call__(self) -> AbstractAsyncContextManager[UnitOfWorkImplementationPort]: ...
