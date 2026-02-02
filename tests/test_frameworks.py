"""Tests for framework endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Framework, Control, FrameworkControl, ControlCategory, ControlType, FrameworkStatus


@pytest.mark.asyncio
async def test_list_frameworks_empty(client: AsyncClient):
    """Test listing frameworks when none exist."""
    response = await client.get("/frameworks")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_frameworks(client: AsyncClient, db_session: AsyncSession):
    """Test listing frameworks."""
    # Create a framework
    framework = Framework(
        code="soc2",
        version="2024",
        name="SOC 2 Type II",
        status=FrameworkStatus.ACTIVE,
    )
    db_session.add(framework)
    await db_session.commit()
    
    response = await client.get("/frameworks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["code"] == "soc2"
    assert data[0]["version"] == "2024"


@pytest.mark.asyncio
async def test_get_framework(client: AsyncClient, db_session: AsyncSession):
    """Test getting a specific framework."""
    framework = Framework(
        code="pci_dss",
        version="v4.0",
        name="PCI DSS",
        status=FrameworkStatus.ACTIVE,
    )
    db_session.add(framework)
    await db_session.commit()
    await db_session.refresh(framework)
    
    response = await client.get(f"/frameworks/{framework.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "pci_dss"
    assert data["version"] == "v4.0"


@pytest.mark.asyncio
async def test_get_framework_not_found(client: AsyncClient):
    """Test getting a non-existent framework."""
    response = await client.get("/frameworks/c303282d-f2e6-46ca-a04a-35d3d873712d")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_framework_controls(client: AsyncClient, db_session: AsyncSession):
    """Test listing controls for a framework."""
    # Create framework
    framework = Framework(
        code="soc2",
        version="2024",
        name="SOC 2 Type II",
        status=FrameworkStatus.ACTIVE,
    )
    db_session.add(framework)
    await db_session.flush()
    
    # Create control
    control = Control(
        code="encrypt_at_rest",
        title="Encryption at Rest",
        description="All data encrypted at rest",
        category=ControlCategory.ENCRYPTION,
        control_type=ControlType.TECHNICAL,
    )
    db_session.add(control)
    await db_session.flush()
    
    # Link control to framework
    fc = FrameworkControl(
        framework_id=framework.id,
        control_id=control.id,
        framework_control_code="CC6.7",
        is_required=True,
    )
    db_session.add(fc)
    await db_session.commit()
    
    response = await client.get(f"/frameworks/{framework.id}/controls")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["code"] == "encrypt_at_rest"
    assert data[0]["framework_control_code"] == "CC6.7"
