import traceback
from typing import Annotated

from fastapi import Depends, HTTPException, status
from orders_service.application.use_cases import OrderUseCases
from orders_service.infrastructure.database import get_db_session
from orders_service.infrastructure.repositories import SQLAlchemyOrderRepository
from sqlalchemy.orm import Session


def get_use_cases(db: Annotated[Session, Depends(get_db_session)]) -> OrderUseCases:
    try:
        repository = SQLAlchemyOrderRepository(session=db)
        return OrderUseCases(repository=repository)
    except Exception as err:
        print("\n" + "=" * 50)
        print("ERROR EN DEPENDENCIES / REPOSITORY:")
        print(traceback.format_exc())
        print("=" * 50 + "\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en get_use_cases: {type(err).__name__} - {err!s}",
        ) from err
