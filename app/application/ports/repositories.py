from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel, NonNegativeInt, PositiveInt

from app.domain.models import Idempotency, Order


class OrderRepository(ABC):
    class CreateDTO(BaseModel):
        user_id: NonNegativeInt
        quantity: PositiveInt
        item_id: UUID

    @abstractmethod
    async def create(self, order: CreateDTO) -> Order:
        pass

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Order | None:
        pass


class IdempotencyRepository(ABC):
    class CreateDTO(BaseModel):
        idempotency_key: UUID
        payload_hash: str
        response: dict

    @abstractmethod
    async def create(self, idempotency: CreateDTO) -> Idempotency: ...

    @abstractmethod
    async def get_by_idempotency_key(
        self, idempotency_key: UUID
    ) -> Idempotency | None: ...
