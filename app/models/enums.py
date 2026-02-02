import enum


class ControlCategory(str, enum.Enum):
    """Category of a control."""

    ACCESS_CONTROL = "access_control"
    ENCRYPTION = "encryption"
    MONITORING = "monitoring"
    CHANGE_MANAGEMENT = "change_management"
    INCIDENT_RESPONSE = "incident_response"
    RISK_ASSESSMENT = "risk_assessment"
    PHYSICAL_SECURITY = "physical_security"
    DATA_PROTECTION = "data_protection"
    NETWORK_SECURITY = "network_security"
    SECURITY_OPERATIONS = "security_operations"
    RISK_MANAGEMENT = "risk_management"
    BUSINESS_CONTINUITY = "business_continuity"
    GOVERNANCE = "governance"
    OTHER = "other"


class ControlType(str, enum.Enum):
    """Type of control."""

    TECHNICAL = "technical"
    ORGANIZATIONAL = "organizational"
    PHYSICAL = "physical"


class FrameworkStatus(str, enum.Enum):
    """Status of a framework version."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    DRAFT = "draft"


class EvidenceType(str, enum.Enum):
    """Type of evidence artifact."""

    SCREENSHOT = "screenshot"
    DOCUMENT = "document"
    LOG_EXPORT = "log_export"
    ATTESTATION = "attestation"
    CONFIGURATION = "configuration"
    POLICY = "policy"
    OTHER = "other"


class EvidenceSource(str, enum.Enum):
    """Source of the evidence."""

    MANUAL = "manual"
    AWS = "aws"
    GITHUB = "github"
    OKTA = "okta"
    OTHER = "other"


class ComplianceStatus(str, enum.Enum):
    """Status of compliance work."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    NOT_APPLICABLE = "not_applicable"
