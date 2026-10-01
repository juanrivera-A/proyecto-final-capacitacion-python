from decimal import Decimal

from orders_service.domain.models import Order, OrderItem
from orders_service.domain.ports import OrderRepository


def test_in_memory_repository_save_and_get(in_memory_repo: OrderRepository) -> None:
    items = [OrderItem(product_id="prod-1", quantity=1, price=Decimal("100.00"))]
    order = Order(customer_id="cust-123", items=items)

    in_memory_repo.save(order)
    retrieved = in_memory_repo.get_by_id(order.id)

    assert retrieved is not None
    assert retrieved.id == order.id
    assert len(in_memory_repo.get_all()) == 1
