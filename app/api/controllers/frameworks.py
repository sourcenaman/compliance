"""Framework API routes."""

import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.base import BaseController
from app.models import Framework, FrameworkControl
from app.schemas import ControlInFramework, FrameworkResponse

logger = logging.getLogger(__name__)


class FrameworkController(BaseController):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def list_frameworks(
        self, code: str | None, status: str | None
    ) -> list[FrameworkResponse]:
        """
        List all frameworks.

        Optionally filter by code (e.g., 'soc2') to get all versions of a framework.
        """
        logger.info(f"Listing frameworks with filters: code={code}, status={status}")

        query = select(Framework)

        if code:
            query = query.where(Framework.code == code)
        if status:
            query = query.where(Framework.status == status)

        query = query.order_by(Framework.code, Framework.version)

        result = await self.db.execute(query)
        frameworks = result.scalars().all()

        return [FrameworkResponse.model_validate(f) for f in frameworks]

    async def get_framework(self, framework_id: int) -> FrameworkResponse:
        """Get a specific framework by ID."""
        logger.info(f"Getting framework {framework_id}")

        result = await self.db.execute(select(Framework).where(Framework.id == framework_id))
        framework = result.scalar_one_or_none()

        if not framework:
            logger.warning(f"Framework {framework_id} not found")
            raise HTTPException(status_code=404, detail="Framework not found")

        return FrameworkResponse.model_validate(framework)

    async def list_framework_controls(self, framework_id: int) -> list[ControlInFramework]:
        """
        List all controls for a specific framework.

        Returns controls with their framework-specific codes (e.g., CC6.1 for SOC 2).
        """
        logger.info(f"Listing controls for framework {framework_id}")

        # First verify framework exists
        framework_result = await self.db.execute(
            select(Framework).where(Framework.id == framework_id)
        )
        if not framework_result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Framework not found")

        # Get framework controls with related control data
        result = await self.db.execute(
            select(FrameworkControl)
            .options(selectinload(FrameworkControl.control))
            .where(FrameworkControl.framework_id == framework_id)
            .order_by(FrameworkControl.framework_control_code)
        )
        framework_controls = result.scalars().all()

        # Build response with control details
        controls = []
        for fc in framework_controls:
            control = fc.control
            controls.append(
                ControlInFramework(
                    id=control.id,
                    code=control.code,
                    title=control.title,
                    description=control.description,
                    category=control.category.value,
                    control_type=control.control_type.value,
                    framework_control_code=fc.framework_control_code,
                    is_required=fc.is_required,
                )
            )

        return controls
