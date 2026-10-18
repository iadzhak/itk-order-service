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
    item_id: str
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if self.quantity < 0:
            raise ValueError('Количество должно быть не отрицательным')
