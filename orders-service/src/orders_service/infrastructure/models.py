from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orders_service.infrastructure.database import Base


class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    customer_id: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    items: Mapped[list["OrderItemModel"]] = relationship(
        "OrderItemModel",
        back_populates="order",
        cascade="all, delete-orphan",
    )


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    order: Mapped[OrderModel] = relationship("OrderModel", back_populates="items")
