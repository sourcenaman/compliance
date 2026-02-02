from pydantic import BaseModel
from app.models.enums import ControlCategory, ControlType


class Control(BaseModel):
    id: str
    code: str
    title: str
    description: str
    category: ControlCategory
    control_type: ControlType


# =============================================================================
# ACCESS CONTROL
# =============================================================================

ctrl_access_restriction = Control(
    id="01944b5a-0002-7000-8000-000000000001",
    code="AC-001",
    title="Logical Access Restriction",
    description="Restrict logical access to information assets to authorized users based on business need-to-know and least privilege principles",
    category=ControlCategory.ACCESS_CONTROL,
    control_type=ControlType.TECHNICAL
)

ctrl_mfa = Control(
    id="01944b5a-0002-7000-8000-000000000002",
    code="AC-002",
    title="Multi-Factor Authentication",
    description="Implement multi-factor authentication for all user access to systems containing sensitive data",
    category=ControlCategory.ACCESS_CONTROL,
    control_type=ControlType.TECHNICAL
)

ctrl_access_review = Control(
    id="01944b5a-0002-7000-8000-000000000003",
    code="AC-003",
    title="User Access Reviews",
    description="Perform periodic reviews of user access rights to ensure access remains appropriate and aligned with job responsibilities",
    category=ControlCategory.ACCESS_CONTROL,
    control_type=ControlType.ORGANIZATIONAL
)

ctrl_physical_access = Control(
    id="01944b5a-0002-7000-8000-000000000004",
    code="AC-004",
    title="Physical Access Control",
    description="Restrict physical access to facilities and systems to authorized personnel only",
    category=ControlCategory.ACCESS_CONTROL,
    control_type=ControlType.PHYSICAL
)

# =============================================================================
# DATA PROTECTION
# =============================================================================

ctrl_encrypt_at_rest = Control(
    id="01944b5a-0002-7000-8000-000000000010",
    code="DP-001",
    title="Encryption at Rest",
    description="Encrypt sensitive data at rest using strong cryptographic algorithms (e.g., AES-256)",
    category=ControlCategory.DATA_PROTECTION,
    control_type=ControlType.TECHNICAL
)

ctrl_encrypt_in_transit = Control(
    id="01944b5a-0002-7000-8000-000000000011",
    code="DP-002",
    title="Encryption in Transit",
    description="Encrypt sensitive data in transit using TLS 1.2 or higher over public networks",
    category=ControlCategory.DATA_PROTECTION,
    control_type=ControlType.TECHNICAL
)

ctrl_key_management = Control(
    id="01944b5a-0002-7000-8000-000000000012",
    code="DP-003",
    title="Cryptographic Key Management",
    description="Establish and maintain a cryptographic key management process including key generation, distribution, storage, rotation, and destruction",
    category=ControlCategory.DATA_PROTECTION,
    control_type=ControlType.ORGANIZATIONAL
)

ctrl_data_classification = Control(
    id="01944b5a-0002-7000-8000-000000000013",
    code="DP-004",
    title="Data Classification",
    description="Classify information assets according to sensitivity and criticality to ensure appropriate protection",
    category=ControlCategory.DATA_PROTECTION,
    control_type=ControlType.ORGANIZATIONAL
)

# =============================================================================
# SECURITY OPERATIONS
# =============================================================================

ctrl_logging = Control(
    id="01944b5a-0002-7000-8000-000000000020",
    code="SO-001",
    title="Security Logging and Monitoring",
    description="Log and monitor all access to systems and sensitive data for security events and anomalies",
    category=ControlCategory.SECURITY_OPERATIONS,
    control_type=ControlType.TECHNICAL
)

ctrl_incident_response = Control(
    id="01944b5a-0002-7000-8000-000000000021",
    code="SO-002",
    title="Incident Response",
    description="Establish and maintain an incident response program to detect, respond to, and recover from security incidents",
    category=ControlCategory.SECURITY_OPERATIONS,
    control_type=ControlType.ORGANIZATIONAL
)

ctrl_vulnerability_mgmt = Control(
    id="01944b5a-0002-7000-8000-000000000022",
    code="SO-003",
    title="Vulnerability Management",
    description="Identify, assess, and remediate security vulnerabilities in systems and applications in a timely manner",
    category=ControlCategory.SECURITY_OPERATIONS,
    control_type=ControlType.TECHNICAL
)

ctrl_malware_protection = Control(
    id="01944b5a-0002-7000-8000-000000000023",
    code="SO-004",
    title="Malware Protection",
    description="Protect systems against malware using anti-malware solutions with regular signature updates",
    category=ControlCategory.SECURITY_OPERATIONS,
    control_type=ControlType.TECHNICAL
)

# =============================================================================
# CHANGE MANAGEMENT
# =============================================================================

ctrl_change_control = Control(
    id="01944b5a-0002-7000-8000-000000000030",
    code="CM-001",
    title="Change Control Process",
    description="Establish a formal change control process for all changes to production systems including testing, approval, and documentation",
    category=ControlCategory.CHANGE_MANAGEMENT,
    control_type=ControlType.ORGANIZATIONAL
)

ctrl_secure_development = Control(
    id="01944b5a-0002-7000-8000-000000000031",
    code="CM-002",
    title="Secure Development Lifecycle",
    description="Implement secure coding practices and security testing throughout the software development lifecycle",
    category=ControlCategory.CHANGE_MANAGEMENT,
    control_type=ControlType.ORGANIZATIONAL
)

# =============================================================================
# RISK MANAGEMENT
# =============================================================================

ctrl_risk_assessment = Control(
    id="01944b5a-0002-7000-8000-000000000040",
    code="RM-001",
    title="Risk Assessment",
    description="Conduct periodic risk assessments to identify, analyze, and evaluate information security risks",
    category=ControlCategory.RISK_MANAGEMENT,
    control_type=ControlType.ORGANIZATIONAL
)

ctrl_vendor_management = Control(
    id="01944b5a-0002-7000-8000-000000000041",
    code="RM-002",
    title="Vendor Risk Management",
    description="Assess and monitor the security posture of third-party vendors and service providers",
    category=ControlCategory.RISK_MANAGEMENT,
    control_type=ControlType.ORGANIZATIONAL
)

# =============================================================================
# BUSINESS CONTINUITY
# =============================================================================

ctrl_backup = Control(
    id="01944b5a-0002-7000-8000-000000000050",
    code="BC-001",
    title="Data Backup and Recovery",
    description="Maintain regular backups of critical data and systems with tested recovery procedures",
    category=ControlCategory.BUSINESS_CONTINUITY,
    control_type=ControlType.TECHNICAL
)

# =============================================================================
# GOVERNANCE
# =============================================================================

ctrl_security_policy = Control(
    id="01944b5a-0002-7000-8000-000000000060",
    code="GV-001",
    title="Information Security Policy",
    description="Establish, communicate, and maintain information security policies approved by management",
    category=ControlCategory.GOVERNANCE,
    control_type=ControlType.ORGANIZATIONAL
)

ctrl_security_awareness = Control(
    id="01944b5a-0002-7000-8000-000000000061",
    code="GV-002",
    title="Security Awareness Training",
    description="Provide security awareness training to all employees upon hire and on an ongoing basis",
    category=ControlCategory.GOVERNANCE,
    control_type=ControlType.ORGANIZATIONAL
)

ctrl_roles_responsibilities = Control(
    id="01944b5a-0002-7000-8000-000000000062",
    code="GV-003",
    title="Roles and Responsibilities",
    description="Define and communicate security roles and responsibilities throughout the organization",
    category=ControlCategory.GOVERNANCE,
    control_type=ControlType.ORGANIZATIONAL
)

# =============================================================================
# NETWORK SECURITY
# =============================================================================

ctrl_network_security = Control(
    id="01944b5a-0002-7000-8000-000000000070",
    code="NS-001",
    title="Network Security Controls",
    description="Install and maintain network security controls (firewalls, IDS/IPS) to protect against unauthorized access",
    category=ControlCategory.NETWORK_SECURITY,
    control_type=ControlType.TECHNICAL
)

ctrl_secure_config = Control(
    id="01944b5a-0002-7000-8000-000000000071",
    code="NS-002",
    title="Secure System Configuration",
    description="Apply secure configurations to all system components, removing unnecessary services and changing default credentials",
    category=ControlCategory.NETWORK_SECURITY,
    control_type=ControlType.TECHNICAL
)

# Export all controls
controls = [
    # Access Control
    ctrl_access_restriction,
    ctrl_mfa,
    ctrl_access_review,
    ctrl_physical_access,
    # Data Protection
    ctrl_encrypt_at_rest,
    ctrl_encrypt_in_transit,
    ctrl_key_management,
    ctrl_data_classification,
    # Security Operations
    ctrl_logging,
    ctrl_incident_response,
    ctrl_vulnerability_mgmt,
    ctrl_malware_protection,
    # Change Management
    ctrl_change_control,
    ctrl_secure_development,
    # Risk Management
    ctrl_risk_assessment,
    ctrl_vendor_management,
    # Business Continuity
    ctrl_backup,
    # Governance
    ctrl_security_policy,
    ctrl_security_awareness,
    ctrl_roles_responsibilities,
    # Network Security
    ctrl_network_security,
    ctrl_secure_config,
]
