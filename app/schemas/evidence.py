"""Evidence Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models import EvidenceSource, EvidenceType


class EvidenceCreate(BaseModel):
    """Schema for creating Evidence."""

    title: str
    description: str | None = None
    evidence_type: EvidenceType = EvidenceType.OTHER
    file_url: str | None = None
    source: EvidenceSource = EvidenceSource.MANUAL
    collected_at: datetime | None = None


class EvidenceResponse(BaseModel):
    """Schema for Evidence response."""

    id: UUID
    organization_id: UUID
    title: str
    description: str | None = None
    evidence_type: EvidenceType
    file_url: str | None = None
    source: EvidenceSource
    collected_at: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ControlEvidenceCreate(BaseModel):
    """Schema for linking evidence to a control."""

    evidence_id: UUID
    linked_by: str | None = None
