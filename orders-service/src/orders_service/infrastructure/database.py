from collections.abc import Generator

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = "sqlite:///./orders.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Requerido solo para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base declarative class for SQLAlchemy ORM models."""


def get_db_session() -> Generator[Session]:
    """Yields a database session and ensures proper cleanup."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en la transacción de BD: {type(err).__name__} - {err!s}",
        ) from err
    finally:
        db.close()
