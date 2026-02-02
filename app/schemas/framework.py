"""Framework Pydantic schemas."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models import FrameworkStatus


class FrameworkBase(BaseModel):
    """Base schema for Framework."""

    code: str
    version: str
    name: str
    description: str | None = None
    status: FrameworkStatus = FrameworkStatus.ACTIVE


class FrameworkCreate(FrameworkBase):
    """Schema for creating a Framework."""

    pass


class FrameworkResponse(FrameworkBase):
    """Schema for Framework response."""

    id: UUID

    model_config = ConfigDict(from_attributes=True)


class ControlInFramework(BaseModel):
    """Schema for a control within a framework context."""

    id: UUID
    code: str
    title: str
    description: str | None = None
    category: str
    control_type: str
    framework_control_code: str
    is_required: bool

    model_config = ConfigDict(from_attributes=True)


class FrameworkControlResponse(BaseModel):
    """Schema for FrameworkControl response."""

    id: UUID
    framework_id: UUID
    control_id: UUID
    framework_control_code: str
    is_required: bool

    model_config = ConfigDict(from_attributes=True)
