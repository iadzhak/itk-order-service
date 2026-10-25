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

    async def notify_new(self, order_id: UUID) -> None:
        await self.notify(
            self.NotificationDTO(
                message='NEW: Ваш заказ создан и ожидает оплаты',
                reference_id=str(order_id),
                idempotency_key=f'{order_id!s}:NEW',
            )
        )

    async def notify_paid(self, order_id: UUID) -> None:
        await self.notify(
            self.NotificationDTO(
                message='PAID: Ваш заказ успешно оплачен и готов к отправке',
                reference_id=str(order_id),
                idempotency_key=f'{order_id!s}:PAID',
            )
        )

    async def notify_shipped(self, order_id: UUID) -> None:
        await self.notify(
            self.NotificationDTO(
                message='SHIPPED: Ваш заказ отправлен в доставку',
                reference_id=str(order_id),
                idempotency_key=f'{order_id!s}:SHIPPED',
            )
        )

    async def notify_cancelled(self, order_id: UUID, reason: str) -> None:
        await self.notify(
            self.NotificationDTO(
                message=f'CANCELLED: Ваш заказ отменен. Причина: {reason}',
                reference_id=str(order_id),
                idempotency_key=f'{order_id!s}:CANCELLED',
            )
        )

    @abstractmethod
    async def notify(self, notification: NotificationDTO) -> None:
        pass
