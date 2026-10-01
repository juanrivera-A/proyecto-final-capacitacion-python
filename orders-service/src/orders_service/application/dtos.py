from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class OrderItemDTO:
    product_id: str
    quantity: int
    price: Decimal


@dataclass(frozen=True)
class CreateOrderInputDTO:
    customer_id: str
    items: list[OrderItemDTO]


@dataclass(frozen=True)
class OrderResponseDTO:
    id: str
    customer_id: str
    status: str
    total_amount: Decimal
    items: list[OrderItemDTO]
