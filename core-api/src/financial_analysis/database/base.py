"""Database base configuration and session management."""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import Generator

from ..config import DATABASE_URL, DB_ECHO

# Create database engine
# connect_args timeout: wait up to 30s for SQLite write locks to clear
# check_same_thread=False: allow SQLAlchemy thread pool to reuse connections safely
engine = create_engine(
    DATABASE_URL,
    echo=DB_ECHO,
    connect_args={"timeout": 30, "check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)

# Enable WAL mode for SQLite to allow concurrent reads during writes
if DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def set_sqlite_pragmas(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create declarative base using SQLAlchemy 2.0 syntax
class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


def get_db() -> Generator[Session, None, None]:
    """
    Get database session.

    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """Initialize database - create all tables."""
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """Drop all database tables."""
    Base.metadata.drop_all(bind=engine)

