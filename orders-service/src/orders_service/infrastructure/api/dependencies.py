from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from orders_service.application.use_cases import OrderUseCases
from orders_service.infrastructure.database import get_db_session
from orders_service.infrastructure.repositories import SQLAlchemyOrderRepository


def get_use_cases(db: Annotated[Session, Depends(get_db_session)]) -> OrderUseCases:
    repository = SQLAlchemyOrderRepository(session=db)
    return OrderUseCases(repository=repository)
