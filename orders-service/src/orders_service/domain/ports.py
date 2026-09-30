from abc import ABC, abstractmethod

from orders_service.domain.models import Order


class OrderRepository(ABC):
    """Abstract port for order persistence operations."""

    @abstractmethod
    def save(self, order: Order) -> None:
        """Persists a new order or updates an existing one."""

    @abstractmethod
    def get_by_id(self, order_id: str) -> Order | None:
        """Retrieves an order by its unique identifier."""

    @abstractmethod
    def get_all(self) -> list[Order]:
        """Retrieves all orders."""
