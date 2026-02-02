from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Organization, OrgFramework
from fastapi import HTTPException

async def get_org_or_404(db: AsyncSession, slug: str) -> Organization:
    """Get organization by slug or raise 404."""
    result = await db.execute(
        select(Organization).where(Organization.slug == slug)
    )
    org = result.scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


async def get_org_framework_or_404(
    db: AsyncSession, 
    org: Organization, 
    framework_id: int
) -> OrgFramework:
    """Get org framework by org and framework_id or raise 404."""
    result = await db.execute(
        select(OrgFramework)
        .where(OrgFramework.organization_id == org.id)
        .where(OrgFramework.framework_id == framework_id)
    )
    org_framework = result.scalar_one_or_none()
    if not org_framework:
        raise HTTPException(status_code=404, detail="Organization has not adopted this framework")
    return org_framework