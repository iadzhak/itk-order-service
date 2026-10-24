from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID


class OrderStatus(StrEnum):
    NEW = 'NEW'
    PAID = 'PAID'
    SHIPPED = 'SHIPPED'
    CANCELLED = 'CANCELLED'


@dataclass
class Order:
    id: UUID
    user_id: str
    quantity: int
    item_id: UUID
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError('Количество должно быть не отрицательным')
        if self.created_at > self.updated_at:
            raise ValueError('Последнее обновление не может быть раньше создания')

    @classmethod
    def from_dict(cls, data: dict) -> Order:
        return cls(
            id=UUID(data['id']),
            user_id=data['user_id'],
            quantity=int(data['quantity']),
            item_id=UUID(data['item_id']),
            status=OrderStatus(data['status']),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
        )

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'user_id': self.user_id,
            'quantity': self.quantity,
            'item_id': str(self.item_id),
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    def set_paid(self) -> None:
        self.status = OrderStatus.PAID

    def set_cancelled(self) -> None:
        self.status = OrderStatus.CANCELLED


@dataclass
class Idempotency:
    idempotency_key: str
    payload_hash: str
    response: dict
    created_at: datetime


class EventType(StrEnum):
    ORDER_PAID = 'order.paid'


class OutboxEventStatus(StrEnum):
    PENDING = 'PENDING'
    SENT = 'SENT'


@dataclass
class OutboxEvent:
    id: int
    event_type: EventType
    payload: dict
    status: OutboxEventStatus
    cerated_at: datetime
