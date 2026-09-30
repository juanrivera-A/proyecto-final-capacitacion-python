from decimal import Decimal

from orders_service.domain.models import Order, OrderItem
from orders_service.domain.ports import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    """In-memory implementation of OrderRepository for testing domain ports."""

    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self._orders[order.id] = order

    def get_by_id(self, order_id: str) -> Order | None:
        return self._orders.get(order_id)

    def get_all(self) -> list[Order]:
        return list(self._orders.values())


def test_in_memory_repository_save_and_get() -> None:
    repo = InMemoryOrderRepository()
    items = [OrderItem(product_id="prod-1", quantity=1, price=Decimal("100.00"))]
    order = Order(customer_id="cust-123", items=items)

    repo.save(order)
    retrieved = repo.get_by_id(order.id)

    assert retrieved is not None
    assert retrieved.id == order.id
    assert len(repo.get_all()) == 1
