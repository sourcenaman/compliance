"""Control Controller."""

from app.base import BaseController
from app.models import Control
from app.schemas.control import ControlResponse
from fastapi import HTTPException
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


logger = logging.getLogger(__name__)


class ControlController(BaseController):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def list_controls(self, category: str | None, control_type: str | None) -> list[ControlResponse]:
        """
        List all controls in the reusable control library.
        
        Controls can be filtered by category or type.
        """
        logger.info(f"Listing controls with filters: category={category}, type={control_type}")
        
        query = select(Control)
        
        if category:
            query = query.where(Control.category == category)
        if control_type:
            query = query.where(Control.control_type == control_type)
        
        query = query.order_by(Control.code)
        
        result = await self.db.execute(query)
        controls = result.scalars().all()
        
        return [ControlResponse.model_validate(c) for c in controls]

    async def get_control(self, code: str) -> ControlResponse:
        """Get a specific control by its code."""
        logger.info(f"Getting control {code}")
        
        result = await self.db.execute(
            select(Control).where(Control.code == code)
        )
        control = result.scalar_one_or_none()
        
        if not control:
            logger.warning(f"Control {code} not found")
            raise HTTPException(status_code=404, detail="Control not found")
        
        return ControlResponse.model_validate(control)

