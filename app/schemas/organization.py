"""Organization Pydantic schemas."""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models import ComplianceStatus


class OrganizationCreate(BaseModel):
    """Schema for creating an Organization."""

    name: str
    slug: str = Field(..., pattern=r"^[a-z0-9-]+$")


class OrganizationResponse(BaseModel):
    """Schema for Organization response."""

    id: UUID
    name: str
    slug: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrgFrameworkCreate(BaseModel):
    """Schema for adopting a framework."""

    framework_id: UUID


class OrgFrameworkResponse(BaseModel):
    """Schema for OrgFramework response."""

    id: UUID
    organization_id: UUID
    framework_id: UUID
    status: ComplianceStatus
    adopted_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrgControlResponse(BaseModel):
    """Schema for OrgControl response."""

    id: UUID
    org_framework_id: UUID
    framework_control_id: UUID
    framework_control_code: str
    control_code: str
    control_title: str
    status: ComplianceStatus
    due_date: date | None = None
    notes: str | None = None
    evidence_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class OrgControlUpdate(BaseModel):
    """Schema for updating an OrgControl."""

    status: ComplianceStatus | None = None
    due_date: date | None = None
    notes: str | None = None
