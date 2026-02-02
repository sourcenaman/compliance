"""Organization API routes."""

import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.base import BaseController
from app.helpers import calculate_readiness, get_org_framework_or_404, get_org_or_404
from app.models import (
    ControlEvidence,
    Evidence,
    Framework,
    FrameworkControl,
    Organization,
    OrgControl,
    OrgFramework,
)
from app.schemas import (
    ControlEvidenceCreate,
    EvidenceCreate,
    EvidenceResponse,
    OrganizationCreate,
    OrganizationResponse,
    OrgControlResponse,
    OrgControlUpdate,
    OrgFrameworkCreate,
    OrgFrameworkResponse,
    ReadinessResponse,
)

logger = logging.getLogger(__name__)

class OrganizationController(BaseController):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create_organization(self, org_data: OrganizationCreate) -> OrganizationResponse:
        """Create a new organization."""
        logger.info(f"Creating organization: {org_data.slug}")

        # Check if slug already exists
        existing = await self.db.execute(
            select(Organization).where(Organization.slug == org_data.slug)
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Organization slug already exists")

        org = Organization(name=org_data.name, slug=org_data.slug)
        self.db.add(org)
        await self.db.flush()
        await self.db.refresh(org)

        logger.info(f"Created organization: {org.id}")
        return OrganizationResponse.model_validate(org)

    async def get_organization(self, slug: str) -> OrganizationResponse:
        """Get organization by slug."""
        logger.info(f"Getting organization: {slug}")
        org = await get_org_or_404(self.db, slug)
        return OrganizationResponse.model_validate(org)

    async def adopt_framework(self, slug: str, data: OrgFrameworkCreate) -> OrgFrameworkResponse:
        """
        Adopt a framework for the organization.

        This creates OrgControl entries for each control in the framework.
        """
        logger.info(f"Organization {slug} adopting framework {data.framework_id}")

        org = await get_org_or_404(self.db, slug)

        # Check framework exists
        framework_result = await self.db.execute(
            select(Framework).where(Framework.id == data.framework_id)
        )
        framework = framework_result.scalar_one_or_none()
        if not framework:
            raise HTTPException(status_code=404, detail="Framework not found")

        # Check if already adopted
        existing = await self.db.execute(
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
        self.db.add(org_framework)
        await self.db.flush()

        # Get all controls for this framework and create OrgControl entries
        fc_result = await self.db.execute(
            select(FrameworkControl).where(FrameworkControl.framework_id == data.framework_id)
        )
        framework_controls = fc_result.scalars().all()

        for fc in framework_controls:
            org_control = OrgControl(
                org_framework_id=org_framework.id,
                framework_control_id=fc.id,
            )
            self.db.add(org_control)

        await self.db.flush()
        await self.db.refresh(org_framework)

        logger.info(f"Organization {slug} adopted framework {framework.code} v{framework.version}")
        return OrgFrameworkResponse.model_validate(org_framework)

    async def list_adopted_frameworks(self, slug: str) -> list[OrgFrameworkResponse]:
        """List all frameworks adopted by the organization."""
        logger.info(f"Listing adopted frameworks for {slug}")

        org = await get_org_or_404(self.db, slug)

        result = await self.db.execute(
            select(OrgFramework)
            .where(OrgFramework.organization_id == org.id)
            .order_by(OrgFramework.adopted_at)
        )
        org_frameworks = result.scalars().all()

        return [OrgFrameworkResponse.model_validate(of) for of in org_frameworks]

    async def list_org_controls(self, slug: str, framework_id: int) -> list[OrgControlResponse]:
        """List all controls for an adopted framework."""
        logger.info(f"Listing controls for {slug} framework {framework_id}")

        org = await get_org_or_404(self.db, slug)
        org_framework = await get_org_framework_or_404(self.db, org, framework_id)

        # Get org controls with related data
        result = await self.db.execute(
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
            controls.append(OrgControlResponse(
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
            ))

        return controls

    async def update_org_control(self, slug: str, control_id: int, data: OrgControlUpdate) -> OrgControlResponse:
        """Update the status or details of an organization's control."""
        logger.info(f"Updating control {control_id} for {slug}")

        org = await get_org_or_404(self.db, slug)

        # Get the org control
        result = await self.db.execute(
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

        await self.db.flush()
        await self.db.refresh(org_control)

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

    async def create_evidence(self, slug: str, data: EvidenceCreate) -> EvidenceResponse:
        """Create a new evidence artifact for the organization."""
        logger.info(f"Creating evidence for {slug}: {data.title}")

        org = await get_org_or_404(self.db, slug)

        evidence = Evidence(
            organization_id=org.id,
            title=data.title,
            description=data.description,
            evidence_type=data.evidence_type,
            file_url=data.file_url,
            source=data.source,
            collected_at=data.collected_at,
        )
        self.db.add(evidence)
        await self.db.flush()
        await self.db.refresh(evidence)

        logger.info(f"Created evidence {evidence.id}")
        return EvidenceResponse.model_validate(evidence)

    async def list_evidence(self, slug: str) -> list[EvidenceResponse]:
        """List all evidence for the organization."""
        logger.info(f"Listing evidence for {slug}")

        org = await get_org_or_404(self.db, slug)

        result = await self.db.execute(
            select(Evidence)
            .where(Evidence.organization_id == org.id)
            .order_by(Evidence.created_at.desc())
        )
        evidence_list = result.scalars().all()

        return [EvidenceResponse.model_validate(e) for e in evidence_list]

    async def link_evidence_to_control(self, slug: str, control_id: int, data: ControlEvidenceCreate) -> dict:
        """Link an evidence artifact to a control."""
        logger.info(f"Linking evidence {data.evidence_id} to control {control_id}")

        org = await get_org_or_404(self.db, slug)

        # Get the org control and verify it belongs to this org
        oc_result = await self.db.execute(
            select(OrgControl)
            .options(selectinload(OrgControl.org_framework))
            .where(OrgControl.id == control_id)
        )
        org_control = oc_result.scalar_one_or_none()

        if not org_control or org_control.org_framework.organization_id != org.id:
            raise HTTPException(status_code=404, detail="Control not found")

        # Verify evidence exists and belongs to this org
        ev_result = await self.db.execute(
            select(Evidence)
            .where(Evidence.id == data.evidence_id)
            .where(Evidence.organization_id == org.id)
        )
        evidence = ev_result.scalar_one_or_none()

        if not evidence:
            raise HTTPException(status_code=404, detail="Evidence not found")

        # Check if already linked
        existing = await self.db.execute(
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
        self.db.add(link)
        await self.db.flush()

        logger.info(f"Linked evidence {data.evidence_id} to control {control_id}")
        return {"message": "Evidence linked successfully"}

    async def get_framework_readiness(self, slug: str, framework_id: int) -> ReadinessResponse:
        """
        Calculate compliance readiness for a framework.

        Returns the percentage of controls that are complete and a list of gaps.
        """
        logger.info(f"Calculating readiness for {slug} framework {framework_id}")

        org = await get_org_or_404(self.db, slug)
        org_framework = await get_org_framework_or_404(self.db, org, framework_id)

        return await calculate_readiness(self.db, org_framework)
