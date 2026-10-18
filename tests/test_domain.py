from datetime import datetime
from uuid import uuid4

import pytest

from app.domain.models import Order, OrderStatus


class TestOrder:

    def test_order_negative_quantity(self):
        with pytest.raises(ValueError):
            order = Order(
                id=uuid4(),
                user_id='',
                quantity=-10,
                item_id='',
                status=OrderStatus.NEW,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )