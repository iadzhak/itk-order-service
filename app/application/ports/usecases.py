import hashlib
from typing import Protocol
from uuid import UUID

from pydantic import BaseModel, NonNegativeInt, PositiveInt

from app.domain.models import Order


class CreateOrderDTO(BaseModel):
    user_id: NonNegativeInt
    quantity: PositiveInt
    item_id: UUID
    idempotency_key: UUID

    def get_hash(self) -> str:
        normalized_data = self.model_dump_json()
        data_bytes = normalized_data.encode('utf-8')
        hash_object = hashlib.sha256(data_bytes)
        return hash_object.hexdigest()


class CreateOrderPort(Protocol):
    async def __call__(self, order: CreateOrderDTO) -> Order: ...


class GetOrderPort(Protocol):
    async def __call__(self, order_id: UUID) -> Order: ...
