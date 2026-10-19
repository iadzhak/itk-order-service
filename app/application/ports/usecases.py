from typing import Protocol
from uuid import UUID

from pydantic import BaseModel, NonNegativeInt, PositiveInt

from app.domain.models import Order


class CreateOrderDTO(BaseModel):
    user_id: NonNegativeInt
    quantity: PositiveInt
    item_id: UUID
    idempotency_key: UUID


class CreateOrderPort(Protocol):
    async def __call__(self, order: CreateOrderDTO) -> Order: ...


class GetOrderPort(Protocol):
    async def __call__(self, order_id: UUID) -> Order: ...
