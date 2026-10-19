from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from app.domain.models import Order, OrderStatus


class TestOrder:
    def test_create_valid(self):
        quantity = 10
        order = Order(
            id=uuid4(),
            user_id=123,
            quantity=quantity,
            item_id=uuid4(),
            status=OrderStatus.NEW,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        assert order.quantity == quantity

    def test_create_negative_quantity(self):
        with pytest.raises(ValueError):
            Order(
                id=uuid4(),
                user_id=123,
                quantity=-10,
                item_id=uuid4(),
                status=OrderStatus.NEW,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

    def test_create_update_before_create_datetime(self):
        with pytest.raises(ValueError):
            Order(
                id=uuid4(),
                user_id=123,
                quantity=-10,
                item_id=uuid4(),
                status=OrderStatus.NEW,
                created_at=datetime.now(),
                updated_at=datetime.now() - timedelta(days=1),
            )
