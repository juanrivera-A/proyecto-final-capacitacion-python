from orders_service.application.dtos import (
    CreateOrderInputDTO,
    OrderItemDTO,
    OrderResponseDTO,
)
from orders_service.domain.exceptions import DomainError
from orders_service.domain.models import Order, OrderItem
from orders_service.domain.ports import OrderRepository


class OrderUseCases:
    """Application service orchestration for order operations."""

    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def create_order(self, input_dto: CreateOrderInputDTO) -> OrderResponseDTO:
        domain_items = [
            OrderItem(
                product_id=item.product_id, quantity=item.quantity, price=item.price
            )
            for item in input_dto.items
        ]
        order = Order(customer_id=input_dto.customer_id, items=domain_items)
        self._repository.save(order)
        return self._to_response_dto(order)

    def pay_order(self, order_id: str) -> OrderResponseDTO:
        order = self._get_order_or_raise(order_id)
        order.pay()
        self._repository.save(order)
        return self._to_response_dto(order)

    def cancel_order(self, order_id: str) -> OrderResponseDTO:
        order = self._get_order_or_raise(order_id)
        order.cancel()
        self._repository.save(order)
        return self._to_response_dto(order)

    def get_order_by_id(self, order_id: str) -> OrderResponseDTO | None:
        order = self._repository.get_by_id(order_id)
        if not order:
            return None
        return self._to_response_dto(order)

    def list_orders(self) -> list[OrderResponseDTO]:
        orders = self._repository.get_all()
        return [self._to_response_dto(order) for order in orders]

    def _get_order_or_raise(self, order_id: str) -> Order:
        order = self._repository.get_by_id(order_id)
        if not order:
            raise DomainError(f"Order with id {order_id} not found.")
        return order

    def _to_response_dto(self, order: Order) -> OrderResponseDTO:
        return OrderResponseDTO(
            id=order.id,
            customer_id=order.customer_id,
            status=order.status.value,
            total_amount=order.total_amount,
            items=[
                OrderItemDTO(
                    product_id=item.product_id, quantity=item.quantity, price=item.price
                )
                for item in order.items
            ],
        )
