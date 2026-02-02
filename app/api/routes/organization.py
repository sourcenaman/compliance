"""Organization API routes."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends

from app.api.controllers import OrganizationController
from app.base import get_controller
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

# ============== Organization Endpoints ==============


@router.post("", response_model=OrganizationResponse, status_code=201)
async def create_organization(
    org_data: OrganizationCreate,
    controller: OrganizationController = Depends(get_controller(OrganizationController)),
) -> OrganizationResponse:
    """Create a new organization."""
    logger.info(f"Creating organization: {org_data.slug}")
    return await controller.create_organization(org_data)


@router.get("/{slug}", response_model=OrganizationResponse)
async def get_organization(
    slug: str,
    controller: OrganizationController = Depends(get_controller(OrganizationController)),
) -> OrganizationResponse:
    """Get organization by slug."""
    logger.info(f"Getting organization: {slug}")
    return await controller.get_organization(slug)


# ============== Framework Adoption Endpoints ==============


@router.post("/{slug}/frameworks", response_model=OrgFrameworkResponse, status_code=201)
async def adopt_framework(
    slug: str,
    data: OrgFrameworkCreate,
    controller: OrganizationController = Depends(get_controller(OrganizationController)),
) -> OrgFrameworkResponse:
    """
    Adopt a framework for the organization.

    This creates OrgControl entries for each control in the framework.
    """
    logger.info(f"Organization {slug} adopting framework {data.framework_id}")
    return await controller.adopt_framework(slug, data)


@router.get("/{slug}/frameworks", response_model=list[OrgFrameworkResponse])
async def list_adopted_frameworks(
    slug: str,
    controller: OrganizationController = Depends(get_controller(OrganizationController)),
) -> list[OrgFrameworkResponse]:
    """List all frameworks adopted by the organization."""
    logger.info(f"Listing adopted frameworks for {slug}")
    return await controller.list_adopted_frameworks(slug)


# ============== Control Status Endpoints ==============


@router.get("/{slug}/frameworks/{framework_id}/controls", response_model=list[OrgControlResponse])
async def list_org_controls(
    slug: str,
    framework_id: UUID,
    controller: OrganizationController = Depends(get_controller(OrganizationController)),
) -> list[OrgControlResponse]:
    """List all controls for an adopted framework."""
    logger.info(f"Listing controls for {slug} framework {framework_id}")
    return await controller.list_org_controls(slug, framework_id)


@router.patch("/{slug}/controls/{control_id}", response_model=OrgControlResponse)
async def update_org_control(
    slug: str,
    control_id: UUID,
    data: OrgControlUpdate,
    controller: OrganizationController = Depends(get_controller(OrganizationController)),
) -> OrgControlResponse:
    """Update the status or details of an organization's control."""
    logger.info(f"Updating control {control_id} for {slug}")
    return await controller.update_org_control(slug, control_id, data)


# ============== Evidence Endpoints ==============


@router.post("/{slug}/evidence", response_model=EvidenceResponse, status_code=201)
async def create_evidence(
    slug: str,
    data: EvidenceCreate,
    controller: OrganizationController = Depends(get_controller(OrganizationController)),
) -> EvidenceResponse:
    """Create a new evidence artifact for the organization."""
    logger.info(f"Creating evidence for {slug}: {data.title}")
    return await controller.create_evidence(slug, data)


@router.get("/{slug}/evidence", response_model=list[EvidenceResponse])
async def list_evidence(
    slug: str,
    controller: OrganizationController = Depends(get_controller(OrganizationController)),
) -> list[EvidenceResponse]:
    """List all evidence for the organization."""
    logger.info(f"Listing evidence for {slug}")
    return await controller.list_evidence(slug)


@router.post("/{slug}/controls/{control_id}/evidence", status_code=201)
async def link_evidence_to_control(
    slug: str,
    control_id: UUID,
    data: ControlEvidenceCreate,
    controller: OrganizationController = Depends(get_controller(OrganizationController)),
) -> dict:
    """Link an evidence artifact to a control."""
    logger.info(f"Linking evidence {data.evidence_id} to control {control_id}")
    return await controller.link_evidence_to_control(slug, control_id, data)


# ============== Readiness Endpoints ==============


@router.get("/{slug}/frameworks/{framework_id}/readiness", response_model=ReadinessResponse)
async def get_framework_readiness(
    slug: str,
    framework_id: UUID,
    controller: OrganizationController = Depends(get_controller(OrganizationController)),
) -> ReadinessResponse:
    """
    Calculate compliance readiness for a framework.

    Returns the percentage of controls that are complete and a list of gaps.
    """
    logger.info(f"Calculating readiness for {slug} framework {framework_id}")
    return await controller.get_framework_readiness(slug, framework_id)
