import pytest

from orders_service.domain.models import Order
from orders_service.domain.ports import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    """In-memory implementation of OrderRepository for testing."""

    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self._orders[order.id] = order

    def get_by_id(self, order_id: str) -> Order | None:
        return self._orders.get(order_id)

    def get_all(self) -> list[Order]:
        return list(self._orders.values())


@pytest.fixture
def in_memory_repo() -> InMemoryOrderRepository:
    return InMemoryOrderRepository()
