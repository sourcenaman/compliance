"""Database connection and session management."""

from sqlalchemy import Column, DateTime, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.sql import func

from app.config import get_settings

settings = get_settings()
sync_db_connection_string = f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

# Create sync engine
sync_engine = create_engine(sync_db_connection_string)
SyncSession: Session = sessionmaker(sync_engine)

async_db_connection_string = f"postgresql+asyncpg://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

# Create async engine
engine = create_async_engine(
    async_db_connection_string,
    echo=settings.debug,
    future=True,
)

# Create async session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    """Dependency that provides a database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Generate table name from class name
    @declared_attr
    def __tablename__(cls) -> str: # noqa: N805
        return cls.__name__.lower()


