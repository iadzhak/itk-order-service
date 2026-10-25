from datetime import datetime
from uuid import UUID, uuid4

from app.application.ports.repositories import (
    IdempotencyRepository,
    InboxRepository,
    OrderRepository,
    OutboxRepository,
)
from app.domain.models import (
    Idempotency,
    InboxEvent,
    InboxEventStatus,
    Order,
    OrderStatus,
    OutboxEvent,
    OutboxEventStatus,
)


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

    async def get_by_id(
        self, order_id: UUID, status: OrderStatus | None = None
    ) -> Order | None:
        return self._orders.get(order_id)

    async def update(self, order: Order) -> Order:
        if order.id not in self._orders:
            raise KeyError(f'Не найден ордер с id {order.id}')
        self._orders[order.id] = order
        return order

    async def mark_as_shipped(self, order_id: UUID) -> None:
        pass

    async def mark_as_cancelled(self, order_id: UUID) -> None:
        pass


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

    async def get_by_idempotency_key(self, idempotency_key: str) -> Idempotency | None:
        return self._idempotency.get(idempotency_key)


class InMemoryOutboxRepository(OutboxRepository):
    def __init__(self, events: dict | None = None) -> None:
        self._events: dict[int, OutboxEvent] = events if events is not None else {}
        self._last_id = 1

    async def create(self, event: OutboxRepository.CreateDTO) -> OutboxEvent:
        while self._last_id in self._events:
            self._last_id += 1
        self._events[self._last_id] = OutboxEvent(
            id=self._last_id,
            event_type=event.event_type,
            payload=event.payload,
            status=OutboxEventStatus.PENDING,
            cerated_at=datetime.now(),
        )
        return self._events[self._last_id]

    async def get_pending_for_update(self, limit: int = 10) -> list[OutboxEvent]:
        res = []
        for event in self._events.values():
            if event.status == OutboxEventStatus.PENDING:
                res.append(event)
            if len(res) >= limit:
                break
        return res

    async def mark_as_sent(self, event_id: int) -> None:
        self._events[event_id].status = OutboxEventStatus.SENT


class InMemoryInboxRepository(InboxRepository):
    def __init__(self, events: dict | None = None) -> None:
        self._events = events if events is not None else {}
        self._last_id = 1

    async def create(self, event: InboxRepository.CreateDTO) -> InboxEvent:
        while self._last_id in self._events:
            self._last_id += 1
        self._events[self._last_id] = InboxEvent(
            id=self._last_id,
            event_id=event.event_id,
            event_type=event.event_type,
            payload=event.payload,
            status=InboxEventStatus.PENDING,
            processed_at=None,
            created_at=datetime.now(),
        )
        return self._events[self._last_id]

    async def get_pending_events(self, limit: int = 10) -> list[InboxEvent]:
        res = []
        for event in self._events.values():
            if event.status == InboxEventStatus.PENDING:
                res.append(event)
            if len(res) >= limit:
                break
        return res

    async def mark_as_processed(self, event_id: int) -> None:
        pass
