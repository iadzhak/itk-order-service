from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel, NonNegativeInt, PositiveInt

from app.domain.models import Order


class OrderRepository(ABC):
    class CreateDTO(BaseModel):
        user_id: NonNegativeInt
        quantity: PositiveInt
        item_id: UUID
        idempotency_key: UUID

    @abstractmethod
    async def create(self, order: CreateDTO) -> Order:
        pass

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Order | None:
        pass
