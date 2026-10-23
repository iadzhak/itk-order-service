from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, NonNegativeInt


class CatalogServicePort(ABC):
    class ItemDTO(BaseModel):
        id: UUID
        name: str
        price: Decimal
        available_qty: NonNegativeInt
        created_at: datetime

    @abstractmethod
    async def get_item(self, item_id: UUID) -> ItemDTO | None:
        pass


class PaymentServicePort(ABC):
    class PaymentDTO(BaseModel):
        order_id: UUID
        amount: Decimal
        callback_url: str
        idempotency_key: str

    class ResponsePaymentDTO(BaseModel):
        id: str
        user_id: str
        order_id: UUID
        amount: Decimal
        status: str
        idempotency_key: str
        created_at: datetime

    @abstractmethod
    async def create_payment(self, data: PaymentDTO) -> bool:
        pass
