"""Readiness calculation service.

This module contains the business logic for calculating compliance readiness.
Separating this from the API layer allows for:
1. Easier unit testing
2. Reusability across different endpoints
3. Clear separation of concerns
"""

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import ComplianceStatus, Framework, FrameworkControl, OrgControl, OrgFramework
from app.schemas.readiness import ControlGap, ReadinessResponse

logger = logging.getLogger(__name__)


async def calculate_readiness(db: AsyncSession, org_framework: OrgFramework) -> ReadinessResponse:
    """
    Calculate compliance readiness for an organization's framework.

    Args:
        db: Database session
        org_framework: The organization's framework adoption record

    Returns:
        ReadinessResponse with statistics and gap list
    """
    logger.info(f"Calculating readiness for org_framework {org_framework.id}")

    # Get framework details
    framework_result = await db.execute(
        select(Framework).where(Framework.id == org_framework.framework_id)
    )
    framework = framework_result.scalar_one()

    # Get all org controls for this framework
    result = await db.execute(
        select(OrgControl)
        .options(selectinload(OrgControl.framework_control).selectinload(FrameworkControl.control))
        .where(OrgControl.org_framework_id == org_framework.id)
    )
    org_controls = result.scalars().all()

    # Calculate statistics
    total = len(org_controls)
    completed = sum(1 for oc in org_controls if oc.status == ComplianceStatus.COMPLETE)
    in_progress = sum(1 for oc in org_controls if oc.status == ComplianceStatus.IN_PROGRESS)
    not_started = sum(1 for oc in org_controls if oc.status == ComplianceStatus.NOT_STARTED)
    not_applicable = sum(1 for oc in org_controls if oc.status == ComplianceStatus.NOT_APPLICABLE)

    # Calculate readiness percentage (excluding N/A)
    applicable_total = total - not_applicable
    if applicable_total > 0:
        readiness_percentage = round((completed / applicable_total) * 100, 1)
    else:
        readiness_percentage = 100.0 if total == 0 else 0.0

    # Find gaps (controls that are not complete or N/A)
    gaps = []
    for oc in org_controls:
        if oc.status not in [ComplianceStatus.COMPLETE, ComplianceStatus.NOT_APPLICABLE]:
            fc = oc.framework_control
            control = fc.control
            gaps.append(
                ControlGap(
                    code=control.code,
                    title=control.title,
                    framework_control_code=fc.framework_control_code,
                    status=oc.status.value,
                )
            )

    logger.info(
        f"Readiness for {framework.code} v{framework.version}: "
        f"{readiness_percentage}% ({completed}/{applicable_total})"
    )

    return ReadinessResponse(
        framework_code=framework.code,
        framework_version=framework.version,
        framework_name=framework.name,
        total_controls=total,
        completed=completed,
        in_progress=in_progress,
        not_started=not_started,
        not_applicable=not_applicable,
        readiness_percentage=readiness_percentage,
        gaps=gaps,
    )
