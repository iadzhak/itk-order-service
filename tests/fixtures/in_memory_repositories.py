from datetime import datetime
from uuid import UUID, uuid4

from app.application.ports.repositories import IdempotencyRepository, OrderRepository
from app.domain.models import Idempotency, Order, OrderStatus


class InMemoryOrderRepository(OrderRepository):
    def __init__(self, orders: dict | None = None):
        self._orders = orders if orders is not None else {}

    async def create(self, order: OrderRepository.CreateDTO) -> Order:
        now = datetime.now()
        db_order = Order(
            id=uuid4(),
            user_id=order.user_id,
            quantity=order.quantity,
            item_id=order.item_id,
            status=OrderStatus.NEW,
            created_at=now,
            updated_at=now,
        )
        self._orders[db_order.id] = db_order
        return db_order

    async def get_by_id(self, order_id: UUID) -> Order | None:
        return self._orders.get(order_id)


class InMemoryIdempotencyRepository(IdempotencyRepository):
    def __init__(self, idempotency: dict | None = None):
        self._idempotency = idempotency if idempotency is not None else {}

    async def create(self, idempotency: IdempotencyRepository.CreateDTO) -> Idempotency:
        db_idempotency = Idempotency(
            idempotency_key=idempotency.idempotency_key,
            payload_hash=idempotency.payload_hash,
            response=idempotency.response,
            created_at=datetime.now(),
        )
        self._idempotency[db_idempotency.idempotency_key] = db_idempotency
        return db_idempotency

    async def get_by_idempotency_key(self, idempotency_key: UUID) -> Idempotency | None:
        return self._idempotency.get(idempotency_key)
