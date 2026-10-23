from datetime import datetime
from uuid import uuid4

import pytest

from app.application.usecases.create_order import CreateOrderDTO, CreateOrderUseCase
from app.application.usecases.get_order import GetOrderUseCase
from app.domain.exceptions import (
    IdempotencyError,
    ItemNotEnoughQuantity,
    ItemNotFound,
    OrderNotFound,
    PaymentServiceError,
)
from app.domain.models import Order, OrderStatus
from tests.fixtures.in_memory_clients import (
    InMemoryCatalogService,
    InMemoryPaymentService,
)
from tests.fixtures.in_memory_uow import InMemoryUnitOfWork


@pytest.mark.asyncio
class TestGetOrderUseCase:
    async def test_exist(self):
        now = datetime.now()
        order = Order(
            id=uuid4(),
            user_id='user_1',
            quantity=10,
            item_id=uuid4(),
            status=OrderStatus.NEW,
            created_at=now,
            updated_at=now,
        )
        uow = InMemoryUnitOfWork()
        uow.orders[order.id] = order

        use_case = GetOrderUseCase(uow)
        found = await use_case(order.id)
        assert isinstance(found, Order)
        assert found.id == order.id
        assert found.user_id == order.user_id
        assert found.quantity == order.quantity
        assert found.item_id == order.item_id
        assert found.status == order.status
        assert found.created_at == order.created_at
        assert found.updated_at == order.updated_at

    async def test_not_exist(self):
        uow = InMemoryUnitOfWork()
        use_case = GetOrderUseCase(uow)
        with pytest.raises(OrderNotFound):
            await use_case(uuid4())


@pytest.mark.asyncio
class TestCreateOrderUseCase:
    def make_catalog_service(self, *items: InMemoryCatalogService.ItemDTO):
        items = {item.id: item for item in items}
        return InMemoryCatalogService(items)

    async def test_success(self):
        new = CreateOrderDTO(
            user_id='user_1',
            quantity=10,
            item_id=uuid4(),
            idempotency_key='test-idempotency-key-123',
        )
        uow = InMemoryUnitOfWork()
        catalog_service = self.make_catalog_service(
            InMemoryCatalogService.ItemDTO(
                id=new.item_id,
                name='abc',
                price=24.6,
                available_qty=new.quantity,
                created_at=datetime.now(),
            )
        )
        use_case = CreateOrderUseCase(
            uow, catalog_service, InMemoryPaymentService(), ''
        )
        created = await use_case(new)
        assert isinstance(created, Order)
        assert created.user_id == new.user_id
        assert created.quantity == new.quantity
        assert created.item_id == new.item_id
        assert created.status == OrderStatus.NEW
        assert new.idempotency_key in uow.idempotency

    async def test_idempotency_success(self):
        new = CreateOrderDTO(
            user_id='user_1',
            quantity=10,
            item_id=uuid4(),
            idempotency_key='test-idempotency-key-123',
        )
        uow = InMemoryUnitOfWork()
        catalog_service = self.make_catalog_service(
            InMemoryCatalogService.ItemDTO(
                id=new.item_id,
                name='abc',
                price=24.6,
                available_qty=new.quantity,
                created_at=datetime.now(),
            )
        )
        use_case = CreateOrderUseCase(
            uow, catalog_service, InMemoryPaymentService(), ''
        )
        found = await use_case(new)
        assert len(uow.idempotency) == 1
        assert len(uow.orders) == 1
        found_2 = await use_case(new)
        assert found == found_2
        assert len(uow.idempotency) == 1
        assert len(uow.orders) == 1

    async def test_idempotency_error(self):
        new = CreateOrderDTO(
            user_id='user_1',
            quantity=10,
            item_id=uuid4(),
            idempotency_key='test-idempotency-key-123',
        )
        uow = InMemoryUnitOfWork()
        catalog_service = self.make_catalog_service(
            InMemoryCatalogService.ItemDTO(
                id=new.item_id,
                name='abc',
                price=24.6,
                available_qty=new.quantity,
                created_at=datetime.now(),
            )
        )
        use_case = CreateOrderUseCase(
            uow, catalog_service, InMemoryPaymentService(), ''
        )
        await use_case(new)
        assert len(uow.idempotency) == 1
        assert len(uow.orders) == 1
        new.quantity += 5
        with pytest.raises(IdempotencyError):
            await use_case(new)

    async def test_item_not_enough_quantity(self):
        new = CreateOrderDTO(
            user_id='user_1',
            quantity=10,
            item_id=uuid4(),
            idempotency_key='test-idempotency-key-123',
        )
        uow = InMemoryUnitOfWork()
        catalog_service = self.make_catalog_service(
            InMemoryCatalogService.ItemDTO(
                id=new.item_id,
                name='abc',
                price=24.6,
                available_qty=new.quantity - 1,
                created_at=datetime.now(),
            )
        )
        use_case = CreateOrderUseCase(
            uow, catalog_service, InMemoryPaymentService(), ''
        )
        with pytest.raises(ItemNotEnoughQuantity):
            await use_case(new)
        assert len(uow.orders) == 0
        assert len(uow.idempotency) == 0

    async def test_item_not_found(self):
        new = CreateOrderDTO(
            user_id='user_1',
            quantity=10,
            item_id=uuid4(),
            idempotency_key='test-idempotency-key-123',
        )
        uow = InMemoryUnitOfWork()
        catalog_service = self.make_catalog_service()
        use_case = CreateOrderUseCase(
            uow, catalog_service, InMemoryPaymentService(), ''
        )
        with pytest.raises(ItemNotFound):
            await use_case(new)
        assert len(uow.orders) == 0
        assert len(uow.idempotency) == 0

    async def test_fail_payment_create(self):
        new = CreateOrderDTO(
            user_id='user_1',
            quantity=10,
            item_id=uuid4(),
            idempotency_key='test-idempotency-key-123',
        )
        uow = InMemoryUnitOfWork()
        catalog_service = self.make_catalog_service(
            InMemoryCatalogService.ItemDTO(
                id=new.item_id,
                name='abc',
                price=24.6,
                available_qty=new.quantity,
                created_at=datetime.now(),
            )
        )
        use_case = CreateOrderUseCase(
            uow, catalog_service, InMemoryPaymentService(False), ''
        )
        with pytest.raises(PaymentServiceError):
            await use_case(new)
