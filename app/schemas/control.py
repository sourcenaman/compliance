"""Control Pydantic schemas."""

from pydantic import BaseModel, ConfigDict
from uuid import UUID
from app.models import ControlCategory, ControlType


class ControlBase(BaseModel):
    """Base schema for Control."""
    code: str
    title: str
    description: str | None = None
    category: ControlCategory = ControlCategory.OTHER
    control_type: ControlType = ControlType.TECHNICAL


class ControlResponse(ControlBase):
    """Schema for Control response."""
    id: UUID
    model_config = ConfigDict(from_attributes=True)
