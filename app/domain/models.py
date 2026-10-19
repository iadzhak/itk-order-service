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
    user_id: int
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
