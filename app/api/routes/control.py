"""Control API routes."""

import logging
from fastapi import APIRouter, Depends, Query
from app.api.controllers import ControlController
from app.base import get_controller
from app.schemas.control import ControlResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=list[ControlResponse])
async def list_controls(
    category: str | None = Query(None, description="Filter by category"),
    control_type: str | None = Query(None, description="Filter by control type"),
    controller: ControlController = Depends(get_controller(ControlController)),
) -> list[ControlResponse]:
    """
    List all controls in the reusable control library.
    
    Controls can be filtered by category or type.
    """
    logger.info(f"Inside the router for list_controls")
    return await controller.list_controls(category, control_type)


@router.get("/{code}", response_model=ControlResponse)
async def get_control(
    code: str,
    controller: ControlController = Depends(get_controller(ControlController)),
) -> ControlResponse:
    """Get a specific control by its code."""
    logger.info(f"Inside the router for get_control")
    return await controller.get_control(code)

