"""Framework API routes."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.api.controllers import FrameworkController
from app.base import get_controller
from app.schemas.framework import ControlInFramework, FrameworkResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=list[FrameworkResponse])
async def list_frameworks(
    code: str | None = Query(None, description="Filter by framework code"),
    status: str | None = Query(None, description="Filter by status"),
    controller: FrameworkController = Depends(get_controller(FrameworkController)),
) -> list[FrameworkResponse]:
    """
    List all frameworks.

    Optionally filter by code (e.g., 'soc2') to get all versions of a framework.
    """
    logger.info(f"Listing frameworks with filters: code={code}, status={status}")
    return await controller.list_frameworks(code, status)


@router.get("/{framework_id}", response_model=FrameworkResponse)
async def get_framework(
    framework_id: UUID,
    controller: FrameworkController = Depends(get_controller(FrameworkController)),
) -> FrameworkResponse:
    """Get a specific framework by ID."""
    logger.info(f"Getting framework {framework_id}")
    return await controller.get_framework(framework_id)


@router.get("/{framework_id}/controls", response_model=list[ControlInFramework])
async def list_framework_controls(
    framework_id: UUID,
    controller: FrameworkController = Depends(get_controller(FrameworkController)),
) -> list[ControlInFramework]:
    """
    List all controls for a specific framework.

    Returns controls with their framework-specific codes (e.g., CC6.1 for SOC 2).
    """
    logger.info(f"Listing controls for framework {framework_id}")

    return await controller.list_framework_controls(framework_id)
