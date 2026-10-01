from sqlalchemy.orm import Session

from orders_service.domain.models import Order, OrderItem, OrderStatus
from orders_service.domain.ports import OrderRepository
from orders_service.infrastructure.models import OrderItemModel, OrderModel


class SQLAlchemyOrderRepository(OrderRepository):
    """SQLAlchemy implementation of the OrderRepository port."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, order: Order) -> None:
        existing_model = self._session.query(OrderModel).filter_by(id=order.id).first()

        if existing_model:
            existing_model.status = order.status.value
            existing_model.items.clear()
            existing_model.items = [
                OrderItemModel(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price,
                )
                for item in order.items
            ]
        else:
            new_model = OrderModel(
                id=order.id,
                customer_id=order.customer_id,
                status=order.status.value,
                items=[
                    OrderItemModel(
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.price,
                    )
                    for item in order.items
                ],
            )
            self._session.add(new_model)

        self._session.commit()

    def get_by_id(self, order_id: str) -> Order | None:
        model = self._session.query(OrderModel).filter_by(id=order_id).first()
        if not model:
            return None
        return self._to_domain(model)

    def get_all(self) -> list[Order]:
        models = self._session.query(OrderModel).all()
        return [self._to_domain(model) for model in models]

    def _to_domain(self, model: OrderModel) -> Order:
        items = [
            OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
            )
            for item in model.items
        ]
        return Order(
            id=model.id,
            customer_id=model.customer_id,
            items=items,
            status=OrderStatus(model.status),
        )
