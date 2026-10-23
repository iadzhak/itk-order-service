import hashlib
from decimal import Decimal
from enum import StrEnum
from typing import Protocol
from uuid import UUID

from pydantic import BaseModel, PositiveInt

from app.domain.models import Order


class CreateOrderDTO(BaseModel):
    user_id: str
    quantity: PositiveInt
    item_id: UUID
    idempotency_key: str

    def get_hash(self) -> str:
        normalized_data = self.model_dump_json()
        data_bytes = normalized_data.encode('utf-8')
        hash_object = hashlib.sha256(data_bytes)
        return hash_object.hexdigest()


class CreateOrderPort(Protocol):
    async def __call__(self, order: CreateOrderDTO) -> Order: ...


class GetOrderPort(Protocol):
    async def __call__(self, order_id: UUID) -> Order: ...


class PaymentDTO(BaseModel):
    payment_id: str
    order_id: UUID
    status: str
    amount: Decimal
    error_message: str


class PaymentStatus(StrEnum):
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'


class PaymentCallbackPort(Protocol):
    async def __call__(self, payment: PaymentDTO) -> Order: ...
