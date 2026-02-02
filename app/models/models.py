from datetime import datetime

from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import true
from uuid_extensions import uuid7

from app.database import Base
from app.models.enums import (
    ComplianceStatus,
    ControlCategory,
    ControlType,
    EvidenceSource,
    EvidenceType,
    FrameworkStatus,
)


class Control(Base):
    """
    A reusable security control.

    Controls are defined once and can be mapped to multiple frameworks.
    This enables control reuse across SOC 2, PCI DSS, ISO 27001, etc.
    """

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("uuidv7()")
    )
    code = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(Enum(ControlCategory), default=ControlCategory.OTHER, nullable=False)
    control_type = Column(Enum(ControlType), default=ControlType.TECHNICAL, nullable=False)

    # Relationships
    framework_controls = relationship(
        "FrameworkControl", back_populates="control", cascade="all, delete-orphan"
    )

    __table_args__ = {"schema": "lookup"}

    def __repr__(self) -> str:
        return f"<Control {self.code}: {self.title}>"


class Framework(Base):
    """
    A compliance framework with version.

    Each row represents a specific version of a framework (e.g., SOC 2 v2024).
    The combination of (code, version) is unique.
    """

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("uuidv7()")
    )
    code = Column(String(50), nullable=False, index=True)
    version = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(FrameworkStatus), default=FrameworkStatus.ACTIVE, nullable=False)

    # Relationships
    framework_controls = relationship(
        "FrameworkControl", back_populates="framework", cascade="all, delete-orphan"
    )
    org_frameworks = relationship("OrgFramework", back_populates="framework")

    __table_args__ = (
        UniqueConstraint("code", "version", name="uq_framework_code_version"),
        {"schema": "lookup"},
    )

    def __repr__(self) -> str:
        return f"<Framework {self.code} v{self.version}>"


class FrameworkControl(Base):
    """
    Junction table linking Controls to Frameworks.

    This allows the same control to be used across multiple frameworks,
    with framework-specific control codes (e.g., CC6.1 for SOC 2, Req 3.5.1 for PCI DSS).
    """

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("uuidv7()")
    )
    framework_id = Column(ForeignKey("lookup.framework.id", ondelete="CASCADE"), nullable=False)
    control_id = Column(ForeignKey("lookup.control.id", ondelete="CASCADE"), nullable=False)
    framework_control_code = Column(
        String(50),
        nullable=False,
        comment="Framework-specific control code (e.g., CC6.1, Req 3.5.1)",
    )
    is_required = Column(Boolean, default=True, nullable=False, server_default=true())

    # Relationships
    framework = relationship("Framework", back_populates="framework_controls")
    control = relationship("Control", back_populates="framework_controls")
    org_controls = relationship("OrgControl", back_populates="framework_control")

    __table_args__ = (
        UniqueConstraint("framework_id", "control_id", name="uq_framework_control"),
        {"schema": "lookup"},
    )

    def __repr__(self) -> str:
        return f"<FrameworkControl {self.framework_control_code}>"


class Evidence(Base):
    """
    A piece of evidence that proves a control is implemented.

    Evidence can be linked to multiple controls across the organization.
    """

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("uuidv7()")
    )
    organization_id = Column(ForeignKey("data.organization.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    evidence_type = Column(Enum(EvidenceType), default=EvidenceType.OTHER, nullable=False)
    file_url = Column(String(500), nullable=True)
    source = Column(Enum(EvidenceSource), default=EvidenceSource.MANUAL, nullable=False)
    collected_at = Column(DateTime, nullable=True)

    # Relationships
    organization = relationship("Organization", back_populates="evidence")
    control_evidence = relationship(
        "ControlEvidence", back_populates="evidence", cascade="all, delete-orphan"
    )

    __table_args__ = {"schema": "data"}

    def __repr__(self) -> str:
        return f"<Evidence {self.id}: {self.title}>"


class ControlEvidence(Base):
    """
    Junction table linking Evidence to OrgControls.

    This allows the same evidence to satisfy multiple controls.
    """

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("uuidv7()")
    )
    org_control_id = Column(ForeignKey("data.orgcontrol.id", ondelete="CASCADE"), nullable=False)
    evidence_id = Column(ForeignKey("data.evidence.id", ondelete="CASCADE"), nullable=False)
    linked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # linked_by = Column(String(100), nullable=True) Enable it when user authentication is implemented

    # Relationships
    org_control = relationship("OrgControl", back_populates="control_evidence")
    evidence = relationship("Evidence", back_populates="control_evidence")

    __table_args__ = {"schema": "data"}

    def __repr__(self) -> str:
        return f"<ControlEvidence control={self.org_control_id} evidence={self.evidence_id}>"


class Organization(Base):
    """
    A company using the compliance platform.

    Organizations can adopt multiple frameworks and track their compliance status.
    """

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("uuidv7()")
    )
    name = Column(String(200), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)

    # Relationships
    org_frameworks = relationship(
        "OrgFramework", back_populates="organization", cascade="all, delete-orphan"
    )
    evidence = relationship("Evidence", back_populates="organization", cascade="all, delete-orphan")

    __table_args__ = {"schema": "data"}

    def __repr__(self) -> str:
        return f"<Organization {self.slug}>"


class OrgFramework(Base):
    """
    A framework adopted by an organization.

    This tracks which frameworks an organization is working towards compliance with.
    """

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("uuidv7()")
    )
    organization_id = Column(ForeignKey("data.organization.id", ondelete="CASCADE"), nullable=False)
    framework_id = Column(ForeignKey("lookup.framework.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(ComplianceStatus), default=ComplianceStatus.NOT_STARTED, nullable=False)
    adopted_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="org_frameworks")
    framework = relationship("Framework", back_populates="org_frameworks")
    org_controls = relationship(
        "OrgControl", back_populates="org_framework", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("organization_id", "framework_id", name="uq_org_framework"),
        {"schema": "data"},
    )

    def __repr__(self) -> str:
        return f"<OrgFramework org={self.organization_id} framework={self.framework_id}>"


class OrgControl(Base):
    """
    An organization's instance of a framework control.

    This tracks the status, owner, and notes for each control
    that an organization is implementing.
    """

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid7, server_default=text("uuidv7()")
    )
    org_framework_id = Column(
        ForeignKey("data.orgframework.id", ondelete="CASCADE"), nullable=False
    )
    framework_control_id = Column(
        ForeignKey("lookup.frameworkcontrol.id", ondelete="CASCADE"), nullable=False
    )
    status = Column(Enum(ComplianceStatus), default=ComplianceStatus.NOT_STARTED, nullable=False)
    # owner_id = Column(String(100), nullable=True) Enable it when user authentication is implemented
    due_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    org_framework = relationship("OrgFramework", back_populates="org_controls")
    framework_control = relationship("FrameworkControl", back_populates="org_controls")
    control_evidence = relationship(
        "ControlEvidence", back_populates="org_control", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("org_framework_id", "framework_control_id", name="uq_org_control"),
        {"schema": "data"},
    )

    def __repr__(self) -> str:
        return f"<OrgControl {self.id} status={self.status}>"
