import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

from orders_service.domain.exceptions import EmptyOrderError, InvalidOrderStateError


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class OrderItem:
    product_id: str
    quantity: int
    price: Decimal

    @property
    def subtotal(self) -> Decimal:
        return self.price * self.quantity


@dataclass
class Order:
    customer_id: str
    items: list[OrderItem]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: OrderStatus = OrderStatus.PENDING

    def __post_init__(self) -> None:
        if not self.items:
            raise EmptyOrderError()

    @property
    def total_amount(self) -> Decimal:
        return sum((item.subtotal for item in self.items), Decimal("0.00"))

    def pay(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise InvalidOrderStateError(
                f"Cannot pay an order with status {self.status.value}"
            )
        self.status = OrderStatus.PAID

    def cancel(self) -> None:
        if self.status == OrderStatus.PAID:
            raise InvalidOrderStateError("Cannot cancel an already paid order")
        self.status = OrderStatus.CANCELLED
