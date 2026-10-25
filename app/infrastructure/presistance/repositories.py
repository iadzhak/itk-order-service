from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.repositories import (
    IdempotencyRepository,
    OrderRepository,
    OutboxRepository,
)
from app.domain.models import (
    Idempotency,
    Order,
    OrderStatus,
    OutboxEvent,
    OutboxEventStatus,
)
from app.infrastructure.presistance.db import Idempotency as IdempotencyORM
from app.infrastructure.presistance.db import Order as OrderORM
from app.infrastructure.presistance.db import Outbox as OutboxORM


class SAOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, order: OrderRepository.CreateDTO) -> Order:
        stmt = (
            insert(OrderORM)
            .values(
                user_id=order.user_id, quantity=order.quantity, item_id=order.item_id
            )
            .returning(OrderORM)
        )
        result = await self._session.execute(stmt)
        db_order = result.scalars().first()
        if not db_order:
            raise RuntimeError('Ошибка создания ордера в базе')
        return self._construct(db_order)

    async def get_by_id(
        self, order_id: UUID, status: OrderStatus | None = None
    ) -> Order | None:
        stmt = select(OrderORM).where(OrderORM.id == order_id)
        if status:
            stmt = stmt.where(OrderORM.status == status)
        result = await self._session.execute(stmt)
        db_order = result.scalars().first()
        if not db_order:
            return None
        return self._construct(db_order)

    async def update(self, order: Order) -> Order:
        stmt = (
            update(OrderORM)
            .where(OrderORM.id == order.id)
            .values(status=order.status)
            .returning(OrderORM)
        )
        result = await self._session.execute(stmt)
        db_order = result.scalars().first()
        if not db_order:
            raise RuntimeError(f'Не удалось выполнить обновление ордера {order.id}')
        return self._construct(db_order)

    @staticmethod
    def _construct(db_order: OrderORM) -> Order:
        return Order(
            id=db_order.id,
            user_id=db_order.user_id,
            quantity=db_order.quantity,
            item_id=db_order.item_id,
            status=db_order.status,
            created_at=db_order.created_at,
            updated_at=db_order.updated_at,
        )


class SAIdempotencyRepository(IdempotencyRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _construct(idempotency: IdempotencyORM) -> Idempotency:
        return Idempotency(
            idempotency_key=idempotency.idempotency_key,
            payload_hash=idempotency.payload_hash,
            response=idempotency.response,
            created_at=idempotency.created_at,
        )

    async def create(self, idempotency: IdempotencyRepository.CreateDTO) -> Idempotency:
        stmt = (
            insert(IdempotencyORM)
            .values(
                idempotency_key=idempotency.idempotency_key,
                payload_hash=idempotency.payload_hash,
                response=idempotency.response,
            )
            .on_conflict_do_nothing(index_elements=['idempotency_key'])
        )
        await self._session.execute(stmt)
        result = await self.get_by_idempotency_key(idempotency.idempotency_key)
        if not result:
            raise RuntimeError('Ошибка создания ключа идемпотентности в базе')
        return result

    async def get_by_idempotency_key(self, idempotency_key: str) -> Idempotency | None:
        stmt = select(IdempotencyORM).where(
            IdempotencyORM.idempotency_key == idempotency_key
        )
        result = await self._session.execute(stmt)
        db_idempotency = result.scalars().first()
        if not db_idempotency:
            return None
        return self._construct(db_idempotency)


class SAOutboxRepository(OutboxRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    @staticmethod
    def _construct(outbox: OutboxORM) -> OutboxEvent:
        return OutboxEvent(
            id=outbox.id,
            event_type=outbox.event_type,
            payload=outbox.payload,
            status=outbox.status,
            cerated_at=outbox.cerated_at,
        )

    async def create(self, event: OutboxRepository.CreateDTO) -> OutboxEvent:
        stmt = (
            insert(OutboxORM)
            .values(event_type=event.event_type, payload=event.payload)
            .returning(OutboxORM)
        )
        result = await self._session.execute(stmt)
        db_event = result.scalars().first()
        if not db_event:
            raise RuntimeError('Ошибка создания outbox event')
        return self._construct(db_event)

    async def get_pending_for_update(self, limit: int = 10) -> list[OutboxEvent]:
        stmt = (
            select(OutboxORM)
            .where(OutboxORM.status == OutboxEventStatus.PENDING)
            .limit(limit)
            .with_for_update(skip_locked=True)
        )
        result = await self._session.execute(stmt)
        db_events = result.scalars().all()
        return [self._construct(db_event) for db_event in db_events]

    async def mark_as_sent(self, event_id: int) -> None:
        stmt = (
            update(OutboxORM)
            .where(OutboxORM.id == event_id)
            .values(status=OutboxEventStatus.SENT)
        )
        await self._session.execute(stmt)
