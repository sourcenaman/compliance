from pydantic import BaseModel

from migrations.seed.control import (
    ctrl_access_restriction,
    ctrl_access_review,
    ctrl_backup,
    ctrl_change_control,
    ctrl_encrypt_at_rest,
    ctrl_encrypt_in_transit,
    ctrl_incident_response,
    ctrl_key_management,
    ctrl_logging,
    ctrl_malware_protection,
    ctrl_mfa,
    ctrl_network_security,
    ctrl_physical_access,
    ctrl_risk_assessment,
    ctrl_roles_responsibilities,
    ctrl_secure_config,
    ctrl_secure_development,
    ctrl_security_awareness,
    ctrl_security_policy,
    ctrl_vendor_management,
    ctrl_vulnerability_mgmt,
)
from migrations.seed.framework import iso27001, pci_dss, soc2


class FrameworkControl(BaseModel):
    id: str
    framework_id: str
    control_id: str
    framework_control_code: str
    is_required: bool


# =============================================================================
# SOC 2 MAPPINGS (Trust Services Criteria - Common Criteria)
# =============================================================================

# CC6 - Logical and Physical Access Controls
soc2_cc6_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000001",
    framework_id=soc2.id,
    control_id=ctrl_access_restriction.id,
    framework_control_code="CC6.1",
    is_required=True
)

soc2_cc6_2 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000002",
    framework_id=soc2.id,
    control_id=ctrl_mfa.id,
    framework_control_code="CC6.2",
    is_required=True
)

soc2_cc6_3 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000003",
    framework_id=soc2.id,
    control_id=ctrl_access_review.id,
    framework_control_code="CC6.3",
    is_required=True
)

soc2_cc6_4 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000004",
    framework_id=soc2.id,
    control_id=ctrl_physical_access.id,
    framework_control_code="CC6.4",
    is_required=True
)

soc2_cc6_7 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000005",
    framework_id=soc2.id,
    control_id=ctrl_encrypt_at_rest.id,
    framework_control_code="CC6.7",
    is_required=True
)

# CC7 - System Operations
soc2_cc7_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000010",
    framework_id=soc2.id,
    control_id=ctrl_vulnerability_mgmt.id,
    framework_control_code="CC7.1",
    is_required=True
)

soc2_cc7_2 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000011",
    framework_id=soc2.id,
    control_id=ctrl_logging.id,
    framework_control_code="CC7.2",
    is_required=True
)

soc2_cc7_4 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000012",
    framework_id=soc2.id,
    control_id=ctrl_incident_response.id,
    framework_control_code="CC7.4",
    is_required=True
)

# CC8 - Change Management
soc2_cc8_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000020",
    framework_id=soc2.id,
    control_id=ctrl_change_control.id,
    framework_control_code="CC8.1",
    is_required=True
)

# CC3 - Risk Assessment
soc2_cc3_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000030",
    framework_id=soc2.id,
    control_id=ctrl_risk_assessment.id,
    framework_control_code="CC3.1",
    is_required=True
)

# CC1 - Control Environment
soc2_cc1_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000040",
    framework_id=soc2.id,
    control_id=ctrl_security_policy.id,
    framework_control_code="CC1.1",
    is_required=True
)

soc2_cc1_4 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000041",
    framework_id=soc2.id,
    control_id=ctrl_security_awareness.id,
    framework_control_code="CC1.4",
    is_required=True
)

# CC9 - Risk Mitigation
soc2_cc9_2 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000050",
    framework_id=soc2.id,
    control_id=ctrl_vendor_management.id,
    framework_control_code="CC9.2",
    is_required=True
)

# =============================================================================
# PCI DSS v4.0 MAPPINGS
# =============================================================================

# Req 1 - Network Security Controls
pci_req1_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000100",
    framework_id=pci_dss.id,
    control_id=ctrl_network_security.id,
    framework_control_code="Req 1.1",
    is_required=True
)

# Req 2 - Secure Configurations
pci_req2_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000101",
    framework_id=pci_dss.id,
    control_id=ctrl_secure_config.id,
    framework_control_code="Req 2.1",
    is_required=True
)

# Req 3 - Protect Stored Data
pci_req3_5 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000102",
    framework_id=pci_dss.id,
    control_id=ctrl_encrypt_at_rest.id,
    framework_control_code="Req 3.5",
    is_required=True
)

pci_req3_6 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000103",
    framework_id=pci_dss.id,
    control_id=ctrl_key_management.id,
    framework_control_code="Req 3.6",
    is_required=True
)

# Req 4 - Encrypt in Transit
pci_req4_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000104",
    framework_id=pci_dss.id,
    control_id=ctrl_encrypt_in_transit.id,
    framework_control_code="Req 4.1",
    is_required=True
)

# Req 5 - Malware Protection
pci_req5_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000105",
    framework_id=pci_dss.id,
    control_id=ctrl_malware_protection.id,
    framework_control_code="Req 5.1",
    is_required=True
)

# Req 6 - Secure Development
pci_req6_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000106",
    framework_id=pci_dss.id,
    control_id=ctrl_secure_development.id,
    framework_control_code="Req 6.1",
    is_required=True
)

pci_req6_2 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000107",
    framework_id=pci_dss.id,
    control_id=ctrl_vulnerability_mgmt.id,
    framework_control_code="Req 6.2",
    is_required=True
)

# Req 7 - Access by Need-to-Know
pci_req7_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000108",
    framework_id=pci_dss.id,
    control_id=ctrl_access_restriction.id,
    framework_control_code="Req 7.1",
    is_required=True
)

# Req 8 - User Authentication
pci_req8_3 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000109",
    framework_id=pci_dss.id,
    control_id=ctrl_mfa.id,
    framework_control_code="Req 8.3",
    is_required=True
)

# Req 9 - Physical Access
pci_req9_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000110",
    framework_id=pci_dss.id,
    control_id=ctrl_physical_access.id,
    framework_control_code="Req 9.1",
    is_required=True
)

# Req 10 - Logging and Monitoring
pci_req10_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000111",
    framework_id=pci_dss.id,
    control_id=ctrl_logging.id,
    framework_control_code="Req 10.1",
    is_required=True
)

# Req 12 - Security Policy
pci_req12_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000112",
    framework_id=pci_dss.id,
    control_id=ctrl_security_policy.id,
    framework_control_code="Req 12.1",
    is_required=True
)

pci_req12_2 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000113",
    framework_id=pci_dss.id,
    control_id=ctrl_risk_assessment.id,
    framework_control_code="Req 12.2",
    is_required=True
)

pci_req12_6 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000114",
    framework_id=pci_dss.id,
    control_id=ctrl_security_awareness.id,
    framework_control_code="Req 12.6",
    is_required=True
)

pci_req12_10 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000115",
    framework_id=pci_dss.id,
    control_id=ctrl_incident_response.id,
    framework_control_code="Req 12.10",
    is_required=True
)

# =============================================================================
# ISO 27001:2022 MAPPINGS (Annex A Controls)
# =============================================================================

# A.5 - Organizational Controls
iso_a5_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000200",
    framework_id=iso27001.id,
    control_id=ctrl_security_policy.id,
    framework_control_code="A.5.1",
    is_required=True
)

iso_a5_2 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000201",
    framework_id=iso27001.id,
    control_id=ctrl_roles_responsibilities.id,
    framework_control_code="A.5.2",
    is_required=True
)

iso_a5_15 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000202",
    framework_id=iso27001.id,
    control_id=ctrl_access_restriction.id,
    framework_control_code="A.5.15",
    is_required=True
)

iso_a5_24 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000203",
    framework_id=iso27001.id,
    control_id=ctrl_incident_response.id,
    framework_control_code="A.5.24",
    is_required=True
)

iso_a5_19 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000204",
    framework_id=iso27001.id,
    control_id=ctrl_vendor_management.id,
    framework_control_code="A.5.19",
    is_required=True
)

# A.6 - People Controls
iso_a6_3 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000210",
    framework_id=iso27001.id,
    control_id=ctrl_security_awareness.id,
    framework_control_code="A.6.3",
    is_required=True
)

# A.7 - Physical Controls
iso_a7_1 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000220",
    framework_id=iso27001.id,
    control_id=ctrl_physical_access.id,
    framework_control_code="A.7.1",
    is_required=True
)

# A.8 - Technological Controls
iso_a8_2 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000230",
    framework_id=iso27001.id,
    control_id=ctrl_access_review.id,
    framework_control_code="A.8.2",
    is_required=True
)

iso_a8_5 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000231",
    framework_id=iso27001.id,
    control_id=ctrl_mfa.id,
    framework_control_code="A.8.5",
    is_required=True
)

iso_a8_7 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000232",
    framework_id=iso27001.id,
    control_id=ctrl_malware_protection.id,
    framework_control_code="A.8.7",
    is_required=True
)

iso_a8_8 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000233",
    framework_id=iso27001.id,
    control_id=ctrl_vulnerability_mgmt.id,
    framework_control_code="A.8.8",
    is_required=True
)

iso_a8_13 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000234",
    framework_id=iso27001.id,
    control_id=ctrl_backup.id,
    framework_control_code="A.8.13",
    is_required=True
)

iso_a8_15 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000235",
    framework_id=iso27001.id,
    control_id=ctrl_logging.id,
    framework_control_code="A.8.15",
    is_required=True
)

iso_a8_20 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000236",
    framework_id=iso27001.id,
    control_id=ctrl_network_security.id,
    framework_control_code="A.8.20",
    is_required=True
)

iso_a8_24 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000237",
    framework_id=iso27001.id,
    control_id=ctrl_encrypt_at_rest.id,
    framework_control_code="A.8.24",
    is_required=True
)

iso_a8_25 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000238",
    framework_id=iso27001.id,
    control_id=ctrl_secure_development.id,
    framework_control_code="A.8.25",
    is_required=True
)

iso_a8_32 = FrameworkControl(
    id="01944b5a-0003-7000-8000-000000000239",
    framework_id=iso27001.id,
    control_id=ctrl_change_control.id,
    framework_control_code="A.8.32",
    is_required=True
)

# =============================================================================
# EXPORT ALL FRAMEWORK CONTROLS
# =============================================================================

framework_controls = [
    # SOC 2
    soc2_cc6_1, soc2_cc6_2, soc2_cc6_3, soc2_cc6_4, soc2_cc6_7,
    soc2_cc7_1, soc2_cc7_2, soc2_cc7_4,
    soc2_cc8_1,
    soc2_cc3_1,
    soc2_cc1_1, soc2_cc1_4,
    soc2_cc9_2,
    # PCI DSS
    pci_req1_1, pci_req2_1,
    pci_req3_5, pci_req3_6,
    pci_req4_1,
    pci_req5_1,
    pci_req6_1, pci_req6_2,
    pci_req7_1,
    pci_req8_3,
    pci_req9_1,
    pci_req10_1,
    pci_req12_1, pci_req12_2, pci_req12_6, pci_req12_10,
    # ISO 27001
    iso_a5_1, iso_a5_2, iso_a5_15, iso_a5_24, iso_a5_19,
    iso_a6_3,
    iso_a7_1,
    iso_a8_2, iso_a8_5, iso_a8_7, iso_a8_8, iso_a8_13, iso_a8_15, iso_a8_20, iso_a8_24, iso_a8_25, iso_a8_32,
]
