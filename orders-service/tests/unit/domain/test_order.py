from decimal import Decimal

import pytest

from orders_service.domain.exceptions import EmptyOrderError
from orders_service.domain.models import Order, OrderItem, OrderStatus


def test_create_order_successfully() -> None:
    items = [
        OrderItem(product_id="prod-1", quantity=2, price=Decimal("100.00")),
        OrderItem(product_id="prod-2", quantity=1, price=Decimal("50.00")),
    ]

    order = Order(customer_id="cust-123", items=items)

    assert order.customer_id == "cust-123"
    assert order.status == OrderStatus.PENDING
    assert order.total_amount == Decimal("250.00")
    assert len(order.items) == 2


def test_create_order_without_items_raises_error() -> None:
    with pytest.raises(EmptyOrderError):
        Order(customer_id="cust-123", items=[])
