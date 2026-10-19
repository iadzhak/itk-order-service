from contextlib import AbstractAsyncContextManager
from typing import Protocol

from app.application.ports.repositories import OrderRepository


class UnitOfWorkImplementationPort(Protocol):
    async def commit(self) -> None: ...

    @property
    def orders(self) -> OrderRepository: ...


UnitOfWorkPort = AbstractAsyncContextManager[UnitOfWorkImplementationPort]
