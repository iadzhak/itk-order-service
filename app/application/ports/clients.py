from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, NonNegativeInt, field_serializer


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

        @field_serializer('amount')
        def serialize_amount(self, v: Decimal, handler) -> str:
            return str(v)

        @field_serializer('order_id')
        def serialize_order_id(self, v: UUID, handler) -> str:
            return str(v)

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


class NotificationServicePort(ABC):
    class NotificationDTO(BaseModel):
        message: str
        reference_id: str
        idempotency_key: str

    @abstractmethod
    async def notify(self, notification: NotificationDTO) -> None:
        pass
