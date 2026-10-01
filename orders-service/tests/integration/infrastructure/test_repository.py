from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from orders_service.domain.models import Order, OrderItem, OrderStatus
from orders_service.infrastructure.database import Base
from orders_service.infrastructure.repositories import SQLAlchemyOrderRepository


@pytest.fixture
def db_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_sqlalchemy_repository_save_and_get(db_session: Session) -> None:
    repo = SQLAlchemyOrderRepository(session=db_session)
    items = [OrderItem(product_id="prod-abc", quantity=2, price=Decimal("250.00"))]
    order = Order(customer_id="cust-xyz", items=items)

    repo.save(order)
    retrieved = repo.get_by_id(order.id)

    assert retrieved is not None
    assert retrieved.id == order.id
    assert retrieved.customer_id == "cust-xyz"
    assert retrieved.status == OrderStatus.PENDING
    assert retrieved.total_amount == Decimal("500.00")


def test_sqlalchemy_repository_update_status(db_session: Session) -> None:
    repo = SQLAlchemyOrderRepository(session=db_session)
    items = [OrderItem(product_id="prod-1", quantity=1, price=Decimal("100.00"))]
    order = Order(customer_id="cust-1", items=items)

    repo.save(order)
    order.pay()
    repo.save(order)

    updated = repo.get_by_id(order.id)
    assert updated is not None
    assert updated.status == OrderStatus.PAID
