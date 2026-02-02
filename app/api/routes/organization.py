"""Organization API routes."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.helpers import calculate_readiness
from app.models import (
    ControlEvidence,
    Evidence,
    Framework,
    FrameworkControl,
    Organization,
    OrgControl,
    OrgFramework,
)
from app.schemas.evidence import ControlEvidenceCreate, EvidenceCreate, EvidenceResponse
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationResponse,
    OrgControlResponse,
    OrgControlUpdate,
    OrgFrameworkCreate,
    OrgFrameworkResponse,
)
from app.schemas.readiness import ReadinessResponse

logger = logging.getLogger(__name__)
router = APIRouter()


# ============== Helper Functions ==============


async def get_org_or_404(db: AsyncSession, slug: str) -> Organization:
    """Get organization by slug or raise 404."""
    result = await db.execute(select(Organization).where(Organization.slug == slug))
    org = result.scalar_one_or_none()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


async def get_org_framework_or_404(
    db: AsyncSession, org: Organization, framework_id: int
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


# ============== Organization Endpoints ==============


@router.post("", response_model=OrganizationResponse, status_code=201)
async def create_organization(
    org_data: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
) -> OrganizationResponse:
    """Create a new organization."""
    logger.info(f"Creating organization: {org_data.slug}")

    # Check if slug already exists
    existing = await db.execute(select(Organization).where(Organization.slug == org_data.slug))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Organization slug already exists")

    org = Organization(name=org_data.name, slug=org_data.slug)
    db.add(org)
    await db.flush()
    await db.refresh(org)

    logger.info(f"Created organization: {org.id}")
    return OrganizationResponse.model_validate(org)


@router.get("/{slug}", response_model=OrganizationResponse)
async def get_organization(
    slug: str,
    db: AsyncSession = Depends(get_db),
) -> OrganizationResponse:
    """Get organization by slug."""
    logger.info(f"Getting organization: {slug}")
    org = await get_org_or_404(db, slug)
    return OrganizationResponse.model_validate(org)


# ============== Framework Adoption Endpoints ==============


@router.post("/{slug}/frameworks", response_model=OrgFrameworkResponse, status_code=201)
async def adopt_framework(
    slug: str,
    data: OrgFrameworkCreate,
    db: AsyncSession = Depends(get_db),
) -> OrgFrameworkResponse:
    """
    Adopt a framework for the organization.

    This creates OrgControl entries for each control in the framework.
    """
    logger.info(f"Organization {slug} adopting framework {data.framework_id}")

    org = await get_org_or_404(db, slug)

    # Check framework exists
    framework_result = await db.execute(select(Framework).where(Framework.id == data.framework_id))
    framework = framework_result.scalar_one_or_none()
    if not framework:
        raise HTTPException(status_code=404, detail="Framework not found")

    # Check if already adopted
    existing = await db.execute(
        select(OrgFramework)
        .where(OrgFramework.organization_id == org.id)
        .where(OrgFramework.framework_id == data.framework_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Framework already adopted")

    # Create OrgFramework
    org_framework = OrgFramework(
        organization_id=org.id,
        framework_id=data.framework_id,
    )
    db.add(org_framework)
    await db.flush()

    # Get all controls for this framework and create OrgControl entries
    fc_result = await db.execute(
        select(FrameworkControl).where(FrameworkControl.framework_id == data.framework_id)
    )
    framework_controls = fc_result.scalars().all()

    for fc in framework_controls:
        org_control = OrgControl(
            org_framework_id=org_framework.id,
            framework_control_id=fc.id,
        )
        db.add(org_control)

    await db.flush()
    await db.refresh(org_framework)

    logger.info(f"Organization {slug} adopted framework {framework.code} v{framework.version}")
    return OrgFrameworkResponse.model_validate(org_framework)


@router.get("/{slug}/frameworks", response_model=list[OrgFrameworkResponse])
async def list_adopted_frameworks(
    slug: str,
    db: AsyncSession = Depends(get_db),
) -> list[OrgFrameworkResponse]:
    """List all frameworks adopted by the organization."""
    logger.info(f"Listing adopted frameworks for {slug}")

    org = await get_org_or_404(db, slug)

    result = await db.execute(
        select(OrgFramework)
        .where(OrgFramework.organization_id == org.id)
        .order_by(OrgFramework.adopted_at)
    )
    org_frameworks = result.scalars().all()

    return [OrgFrameworkResponse.model_validate(of) for of in org_frameworks]


# ============== Control Status Endpoints ==============


@router.get("/{slug}/frameworks/{framework_id}/controls", response_model=list[OrgControlResponse])
async def list_org_controls(
    slug: str,
    framework_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> list[OrgControlResponse]:
    """List all controls for an adopted framework."""
    logger.info(f"Listing controls for {slug} framework {framework_id}")

    org = await get_org_or_404(db, slug)
    org_framework = await get_org_framework_or_404(db, org, framework_id)

    # Get org controls with related data
    result = await db.execute(
        select(OrgControl)
        .options(
            selectinload(OrgControl.framework_control).selectinload(FrameworkControl.control),
            selectinload(OrgControl.control_evidence),
        )
        .where(OrgControl.org_framework_id == org_framework.id)
    )
    org_controls = result.scalars().all()

    # Build response
    controls = []
    for oc in org_controls:
        fc = oc.framework_control
        control = fc.control
        controls.append(
            OrgControlResponse(
                id=oc.id,
                org_framework_id=oc.org_framework_id,
                framework_control_id=oc.framework_control_id,
                framework_control_code=fc.framework_control_code,
                control_code=control.code,
                control_title=control.title,
                status=oc.status,
                owner_id=oc.owner_id,
                due_date=oc.due_date,
                notes=oc.notes,
                evidence_count=len(oc.control_evidence),
            )
        )

    return controls


@router.patch("/{slug}/controls/{control_id}", response_model=OrgControlResponse)
async def update_org_control(
    slug: str,
    control_id: UUID,
    data: OrgControlUpdate,
    db: AsyncSession = Depends(get_db),
) -> OrgControlResponse:
    """Update the status or details of an organization's control."""
    logger.info(f"Updating control {control_id} for {slug}")

    org = await get_org_or_404(db, slug)

    # Get the org control
    result = await db.execute(
        select(OrgControl)
        .options(
            selectinload(OrgControl.org_framework),
            selectinload(OrgControl.framework_control).selectinload(FrameworkControl.control),
            selectinload(OrgControl.control_evidence),
        )
        .where(OrgControl.id == control_id)
    )
    org_control = result.scalar_one_or_none()

    if not org_control:
        raise HTTPException(status_code=404, detail="Control not found")

    # Verify it belongs to this org
    if org_control.org_framework.organization_id != org.id:
        raise HTTPException(status_code=404, detail="Control not found")

    # Update fields
    if data.status is not None:
        org_control.status = data.status
    if data.owner_id is not None:
        org_control.owner_id = data.owner_id
    if data.due_date is not None:
        org_control.due_date = data.due_date
    if data.notes is not None:
        org_control.notes = data.notes

    await db.flush()
    await db.refresh(org_control)

    fc = org_control.framework_control
    control = fc.control

    return OrgControlResponse(
        id=org_control.id,
        org_framework_id=org_control.org_framework_id,
        framework_control_id=org_control.framework_control_id,
        framework_control_code=fc.framework_control_code,
        control_code=control.code,
        control_title=control.title,
        status=org_control.status,
        owner_id=org_control.owner_id,
        due_date=org_control.due_date,
        notes=org_control.notes,
        evidence_count=len(org_control.control_evidence),
    )


# ============== Evidence Endpoints ==============


@router.post("/{slug}/evidence", response_model=EvidenceResponse, status_code=201)
async def create_evidence(
    slug: str,
    data: EvidenceCreate,
    db: AsyncSession = Depends(get_db),
) -> EvidenceResponse:
    """Create a new evidence artifact for the organization."""
    logger.info(f"Creating evidence for {slug}: {data.title}")

    org = await get_org_or_404(db, slug)

    evidence = Evidence(
        organization_id=org.id,
        title=data.title,
        description=data.description,
        evidence_type=data.evidence_type,
        file_url=data.file_url,
        source=data.source,
        collected_at=data.collected_at,
    )
    db.add(evidence)
    await db.flush()
    await db.refresh(evidence)

    logger.info(f"Created evidence {evidence.id}")
    return EvidenceResponse.model_validate(evidence)


@router.get("/{slug}/evidence", response_model=list[EvidenceResponse])
async def list_evidence(
    slug: str,
    db: AsyncSession = Depends(get_db),
) -> list[EvidenceResponse]:
    """List all evidence for the organization."""
    logger.info(f"Listing evidence for {slug}")

    org = await get_org_or_404(db, slug)

    result = await db.execute(
        select(Evidence)
        .where(Evidence.organization_id == org.id)
        .order_by(Evidence.created_at.desc())
    )
    evidence_list = result.scalars().all()

    return [EvidenceResponse.model_validate(e) for e in evidence_list]


@router.post("/{slug}/controls/{control_id}/evidence", status_code=201)
async def link_evidence_to_control(
    slug: str,
    control_id: UUID,
    data: ControlEvidenceCreate,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Link an evidence artifact to a control."""
    logger.info(f"Linking evidence {data.evidence_id} to control {control_id}")

    org = await get_org_or_404(db, slug)

    # Get the org control and verify it belongs to this org
    oc_result = await db.execute(
        select(OrgControl)
        .options(selectinload(OrgControl.org_framework))
        .where(OrgControl.id == control_id)
    )
    org_control = oc_result.scalar_one_or_none()

    if not org_control or org_control.org_framework.organization_id != org.id:
        raise HTTPException(status_code=404, detail="Control not found")

    # Verify evidence exists and belongs to this org
    ev_result = await db.execute(
        select(Evidence)
        .where(Evidence.id == data.evidence_id)
        .where(Evidence.organization_id == org.id)
    )
    evidence = ev_result.scalar_one_or_none()

    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")

    # Check if already linked
    existing = await db.execute(
        select(ControlEvidence)
        .where(ControlEvidence.org_control_id == control_id)
        .where(ControlEvidence.evidence_id == data.evidence_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Evidence already linked to this control")

    # Create link
    link = ControlEvidence(
        org_control_id=control_id,
        evidence_id=data.evidence_id,
        linked_by=data.linked_by,
    )
    db.add(link)
    await db.flush()

    logger.info(f"Linked evidence {data.evidence_id} to control {control_id}")
    return {"message": "Evidence linked successfully"}


# ============== Readiness Endpoints ==============


@router.get("/{slug}/frameworks/{framework_id}/readiness", response_model=ReadinessResponse)
async def get_framework_readiness(
    slug: str,
    framework_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ReadinessResponse:
    """
    Calculate compliance readiness for a framework.

    Returns the percentage of controls that are complete and a list of gaps.
    """
    logger.info(f"Calculating readiness for {slug} framework {framework_id}")

    org = await get_org_or_404(db, slug)
    org_framework = await get_org_framework_or_404(db, org, framework_id)

    return await calculate_readiness(db, org_framework)
