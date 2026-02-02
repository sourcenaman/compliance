"""Readiness Pydantic schemas."""

from pydantic import BaseModel


class ControlGap(BaseModel):
    """A control that is missing evidence or not complete."""

    code: str
    title: str
    framework_control_code: str
    status: str


class ReadinessResponse(BaseModel):
    """Schema for readiness calculation response."""

    framework_code: str
    framework_version: str
    framework_name: str
    total_controls: int
    completed: int
    in_progress: int
    not_started: int
    not_applicable: int
    readiness_percentage: float
    gaps: list[ControlGap]
