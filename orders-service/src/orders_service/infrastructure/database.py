from collections.abc import Generator

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
    finally:
        db.close()
