"""Database connection and session management.

Key principle: Pool is lifespan-scoped, Session is request-scoped.
- Engine/pool: created once in init_db(), disposed in close_db()
- Session: created per-request via get_db() dependency
"""

from sqlalchemy import Column, DateTime, create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.sql import func

from app.config import get_settings

# Module-level references, initialized during app lifespan
engine: AsyncEngine | None = None
async_session: async_sessionmaker[AsyncSession] | None = None
sync_engine = None
SyncSession = None


async def init_db():
    """Initialize database engines and session factories. Called at app startup."""
    global engine, async_session, sync_engine, SyncSession

    settings = get_settings()

    sync_db_connection_string = f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
    sync_engine = create_engine(sync_db_connection_string)
    SyncSession = sessionmaker(sync_engine)
    print(SyncSession)

    async_db_connection_string = f"postgresql+asyncpg://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
    engine = create_async_engine(
        async_db_connection_string,
        echo=settings.debug,
        future=True,
    )
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def close_db():
    """Dispose database engines. Called at app shutdown."""
    global engine, sync_engine, SyncSession
    if engine:
        await engine.dispose()
        engine = None
    if sync_engine:
        sync_engine.dispose()
        sync_engine = None


async def get_db() -> AsyncSession:
    """Dependency that provides a database session (one per request)."""
    if async_session is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
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
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Generate table name from class name
    @declared_attr
    def __tablename__(cls) -> str:  # noqa: N805
        return cls.__name__.lower()
