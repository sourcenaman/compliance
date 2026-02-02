from pydantic import BaseModel
from app.models.enums import FrameworkStatus


class Framework(BaseModel):
    id: str
    code: str
    version: str
    name: str
    description: str
    status: FrameworkStatus


# SOC 2 Framework
soc2 = Framework(
    id="01944b5a-0001-7000-8000-000000000001",
    code="SOC2",
    version="2024",
    name="SOC 2 Type II",
    description="Service Organization Control 2 - Trust Services Criteria for Security, Availability, Processing Integrity, Confidentiality, and Privacy",
    status=FrameworkStatus.ACTIVE
)

# PCI DSS Framework
pci_dss = Framework(
    id="01944b5a-0001-7000-8000-000000000002",
    code="PCI-DSS",
    version="4.0",
    name="PCI DSS v4.0",
    description="Payment Card Industry Data Security Standard - Security requirements for organizations handling credit card data",
    status=FrameworkStatus.ACTIVE
)

# ISO 27001 Framework
iso27001 = Framework(
    id="01944b5a-0001-7000-8000-000000000003",
    code="ISO27001",
    version="2022",
    name="ISO/IEC 27001:2022",
    description="Information Security Management System (ISMS) - International standard for information security with 93 controls in 4 categories",
    status=FrameworkStatus.ACTIVE
)


frameworks = [soc2, pci_dss, iso27001]