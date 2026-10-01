from decimal import Decimal

import pytest

from orders_service.application.dtos import CreateOrderInputDTO, OrderItemDTO
from orders_service.application.use_cases import OrderUseCases
from orders_service.domain.exceptions import DomainError
from orders_service.domain.ports import OrderRepository


@pytest.fixture
def use_cases(in_memory_repo: OrderRepository) -> OrderUseCases:
    return OrderUseCases(repository=in_memory_repo)


def test_create_order_use_case(use_cases: OrderUseCases) -> None:
    input_dto = CreateOrderInputDTO(
        customer_id="cust-001",
        items=[
            OrderItemDTO(product_id="prod-100", quantity=2, price=Decimal("150.00"))
        ],
    )

    response = use_cases.create_order(input_dto)

    assert response.customer_id == "cust-001"
    assert response.status == "PENDING"
    assert response.total_amount == Decimal("300.00")


def test_pay_order_use_case(use_cases: OrderUseCases) -> None:
    input_dto = CreateOrderInputDTO(
        customer_id="cust-001",
        items=[OrderItemDTO(product_id="prod-100", quantity=1, price=Decimal("50.00"))],
    )
    created = use_cases.create_order(input_dto)

    paid_response = use_cases.pay_order(created.id)

    assert paid_response.status == "PAID"


def test_pay_non_existent_order_raises_error(use_cases: OrderUseCases) -> None:
    with pytest.raises(DomainError):
        use_cases.pay_order("non-existent-id")
