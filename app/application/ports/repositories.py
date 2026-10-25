from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel, PositiveInt

from app.domain.models import (
    EventType,
    Idempotency,
    Order,
    OrderStatus,
    OutboxEvent,
)


class OrderRepository(ABC):
    class CreateDTO(BaseModel):
        user_id: str
        quantity: PositiveInt
        item_id: UUID

    @abstractmethod
    async def create(self, order: CreateDTO) -> Order:
        pass

    @abstractmethod
    async def get_by_id(
        self, order_id: UUID, status: OrderStatus | None = None
    ) -> Order | None:
        pass

    @abstractmethod
    async def update(self, order: Order) -> Order:
        pass


class IdempotencyRepository(ABC):
    class CreateDTO(BaseModel):
        idempotency_key: str
        payload_hash: str
        response: dict

    @abstractmethod
    async def create(self, idempotency: CreateDTO) -> Idempotency: ...

    @abstractmethod
    async def get_by_idempotency_key(
        self, idempotency_key: str
    ) -> Idempotency | None: ...


class OutboxRepository(ABC):
    class CreateDTO(BaseModel):
        event_type: EventType
        payload: dict

    @abstractmethod
    async def create(self, event: CreateDTO) -> OutboxEvent:
        pass

    @abstractmethod
    async def get_pending_for_update(self, limit: int = 10) -> list[OutboxEvent]:
        pass

    @abstractmethod
    async def mark_as_sent(self, event_id: int) -> None:
        pass
