"""Test configuration and fixtures."""

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import Base, get_db
from app.main import app
from app.models import (
    Control,
    ControlCategory,
    ControlType,
    Framework,
    FrameworkControl,
    FrameworkStatus,
    Organization,
)

# Use PostgreSQL for tests (matches production, supports UUID)
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/compliance_test"

engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
)
TestingSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database for each test."""
    async with engine.begin() as conn:
        # Create schemas first (required for tables in lookup/data schemas)
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS lookup"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS data"))
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS audit"))
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with database override."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def seeded_db(db_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    """Database session with pre-seeded test data."""

    # Create frameworks
    soc2 = Framework(
        code="soc2",
        version="2024",
        name="SOC 2 Type II",
        description="Service Organization Control 2",
        status=FrameworkStatus.ACTIVE
    )
    pci_dss = Framework(
        code="pci_dss",
        version="v4.0",
        name="PCI DSS",
        description="Payment Card Industry Data Security Standard",
        status=FrameworkStatus.ACTIVE
    )
    db_session.add_all([soc2, pci_dss])
    await db_session.flush()

    # Create controls
    encrypt_at_rest = Control(
        code="encrypt_at_rest",
        title="Encryption at Rest",
        description="All data must be encrypted at rest",
        category=ControlCategory.ENCRYPTION,
        control_type=ControlType.TECHNICAL
    )
    mfa_required = Control(
        code="mfa_required",
        title="Multi-Factor Authentication",
        description="MFA must be enabled for all users",
        category=ControlCategory.ACCESS_CONTROL,
        control_type=ControlType.TECHNICAL
    )
    access_review = Control(
        code="access_review",
        title="Access Review",
        description="Quarterly access reviews required",
        category=ControlCategory.ACCESS_CONTROL,
        control_type=ControlType.ORGANIZATIONAL
    )
    db_session.add_all([encrypt_at_rest, mfa_required, access_review])
    await db_session.flush()

    # Map controls to frameworks
    fc1 = FrameworkControl(
        framework_id=soc2.id,
        control_id=encrypt_at_rest.id,
        framework_control_code="CC6.7",
        is_required=True
    )
    fc2 = FrameworkControl(
        framework_id=soc2.id,
        control_id=mfa_required.id,
        framework_control_code="CC6.1",
        is_required=True
    )
    fc3 = FrameworkControl(
        framework_id=pci_dss.id,
        control_id=encrypt_at_rest.id,
        framework_control_code="Req 3.5.1",
        is_required=True
    )
    db_session.add_all([fc1, fc2, fc3])

    # Create a test organization
    org = Organization(
        name="Test Company",
        slug="test-company"
    )
    db_session.add(org)

    await db_session.commit()

    yield db_session


@pytest_asyncio.fixture
async def seeded_client(seeded_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Test client with seeded database."""
    async def override_get_db():
        yield seeded_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()

