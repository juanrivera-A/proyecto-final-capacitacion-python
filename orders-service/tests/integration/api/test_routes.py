from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from orders_service.infrastructure.database import Base, get_db_session
from orders_service.main import app


@pytest.fixture
def db_session() -> Generator[Session]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient]:
    def _override_get_db_session() -> Generator[Session]:
        yield db_session

    app.dependency_overrides[get_db_session] = _override_get_db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_order_api(client: TestClient) -> None:
    payload = {
        "customer_id": "cust-http-1",
        "items": [{"product_id": "prod-1", "quantity": 2, "price": 100.0}],
    }
    create_res = client.post("/orders", json=payload)
    assert create_res.status_code == 201
    data = create_res.json()
    assert data["customer_id"] == "cust-http-1"
    assert data["total_amount"] == "200.00"

    order_id = data["id"]
    get_res = client.get(f"/orders/{order_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == order_id


def test_pay_order_api(client: TestClient) -> None:
    payload = {
        "customer_id": "cust-http-2",
        "items": [{"product_id": "prod-1", "quantity": 1, "price": 50.0}],
    }
    create_res = client.post("/orders", json=payload)
    order_id = create_res.json()["id"]

    pay_res = client.post(f"/orders/{order_id}/pay")
    assert pay_res.status_code == 200
    assert pay_res.json()["status"] == "PAID"
