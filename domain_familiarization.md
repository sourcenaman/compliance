# Phase 0: Domain Familiarization
> **Purpose:** Understand compliance frameworks well enough to design a config-driven RMF engine  
> **Time Budget:** ~4 hours  
> **Goal:** Extract patterns, not memorize standards

---

## 1. What is Compliance Automation?

Compliance automation helps companies **prove they're secure** to customers, auditors, and regulators by:
- Tracking which security **controls** they need to implement
- Collecting **evidence** that controls are met
- Generating **reports** for audits

**Who needs it?** Any company handling sensitive data (payments, health records, customer PII) that wants to do business with enterprises.

---

## 2. Key Frameworks Overview

### 2.1 SOC 2 (Service Organization Control 2)

**What it is:** An auditing standard by AICPA for service providers storing customer data in the cloud.

**Who needs it:** SaaS companies, cloud providers, any tech company handling customer data.

**Structure:**

```
SOC 2
├── Trust Services Criteria (5 categories)
│   ├── Security (CC) ─── MANDATORY for all SOC 2 reports
│   ├── Availability (A)
│   ├── Processing Integrity (PI)
│   ├── Confidentiality (C)
│   └── Privacy (P)
│
└── Common Criteria (CC1-CC9) under Security
    ├── CC1: Control Environment
    ├── CC2: Communication & Information
    ├── CC3: Risk Assessment
    ├── CC4: Monitoring Activities
    ├── CC5: Control Activities
    ├── CC6: Logical & Physical Access Controls
    ├── CC7: System Operations
    ├── CC8: Change Management
    └── CC9: Risk Mitigation
```

**Key Insight:** Security is the foundation; other categories are optional based on business needs.

---

### 2.2 PCI DSS (Payment Card Industry Data Security Standard)

**What it is:** Security standard for organizations handling credit card data.

**Who needs it:** Any business that processes, stores, or transmits cardholder data.

**Structure:**

```
PCI DSS v4.0
├── Goal 1: Build and Maintain a Secure Network
│   ├── Req 1: Install and maintain network security controls
│   └── Req 2: Apply secure configurations to all systems
│
├── Goal 2: Protect Cardholder Data
│   ├── Req 3: Protect stored account data
│   └── Req 4: Encrypt data over public networks
│
├── Goal 3: Maintain a Vulnerability Management Program
│   ├── Req 5: Protect systems from malware
│   └── Req 6: Develop and maintain secure systems
│
├── Goal 4: Implement Strong Access Control
│   ├── Req 7: Restrict access by business need-to-know
│   ├── Req 8: Identify users and authenticate access
│   └── Req 9: Restrict physical access
│
├── Goal 5: Monitor and Test Networks
│   ├── Req 10: Log and monitor all access
│   └── Req 11: Test security regularly
│
└── Goal 6: Maintain Information Security Policy
    └── Req 12: Support security with organizational policies
```

**Key Insight:** 12 requirements grouped into 6 logical goals. Very prescriptive compared to SOC 2.

---

### 2.3 ISO 27001 (Information Security Management System)

**What it is:** International standard for establishing, implementing, and maintaining an ISMS.

**Who needs it:** Organizations seeking international certification for information security.

**Structure (2022 version):**

```
ISO 27001:2022 Annex A
├── Organizational Controls (37 controls)
│   ├── Policies, governance, roles & responsibilities
│   ├── Segregation of duties
│   └── Threat intelligence
│
├── People Controls (8 controls)
│   ├── Screening, awareness, training
│   └── Remote working policies
│
├── Physical Controls (14 controls)
│   ├── Security perimeters
│   ├── Physical entry controls
│   └── Equipment security
│
└── Technological Controls (34 controls)
    ├── Authentication & access management
    ├── Cryptography & encryption
    ├── Secure development
    └── Data leakage prevention
```

**Key Insight:** 93 controls in 4 categories. Organizations select controls based on their risk assessment.

---

### 2.4 NIST Risk Management Framework (RMF)

**What it is:** A framework by NIST for integrating security and risk management into the system development lifecycle.

**Structure:**

```
NIST RMF Steps
1. Categorize → Classify system based on impact
2. Select → Choose security controls
3. Implement → Put controls in place
4. Assess → Evaluate control effectiveness
5. Authorize → Accept residual risk
6. Monitor → Continuously track security state
```

**Key Insight:** It's a *process* framework, not a control list. Provides conceptual grounding for how risk management works.

---

## 3. How Frameworks Are Organized (The Hierarchy)

All compliance frameworks follow a similar **hierarchical structure**:

```
Framework
└── Domain / Category
    └── Control
        └── Requirement (specific aspect)
            └── Evidence (proof of implementation)
```

### 3.1 The Hierarchy Explained

| Level | What It Is | Example |
|-------|-----------|---------|
| **Framework** | The compliance standard itself | SOC 2, PCI DSS, ISO 27001 |
| **Domain/Category** | A logical grouping of related controls | "Security", "Access Control", "Physical Security" |
| **Control** | A specific security requirement | "Encrypt data at rest" |
| **Requirement** | A sub-aspect or test within a control | "Use AES-256 encryption" |
| **Evidence** | Proof that the requirement is met | Screenshot of S3 encryption settings |

---

### 3.2 Concrete Examples from Each Framework

#### SOC 2 Example

```
Framework: SOC 2
└── Domain: Security (Common Criteria)
    └── Control: CC6.1 - Logical Access Security
        └── Requirement: "The entity restricts logical access to 
                         information assets to authorized users"
            └── Evidence:
                ├── AWS IAM policy export
                ├── User access review logs
                └── MFA configuration screenshot
```

#### PCI DSS Example

```
Framework: PCI DSS v4.0
└── Goal/Domain: Protect Cardholder Data
    └── Requirement: Req 3 - Protect stored account data
        └── Sub-requirement: 3.5.1 - Encrypt PAN using strong cryptography
            └── Evidence:
                ├── Database encryption configuration
                ├── Key management policy document
                └── Encryption algorithm documentation
```

#### ISO 27001 Example

```
Framework: ISO 27001:2022
└── Category: Technological Controls
    └── Control: A.8.24 - Use of cryptography
        └── Implementation Guidance: "Cryptographic controls shall be 
                                      implemented based on a policy"
            └── Evidence:
                ├── Cryptography policy document
                ├── Certificate inventory
                └── TLS configuration screenshots
```

---

### 3.3 Visual Representation

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRAMEWORK (SOC 2)                           │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │               DOMAIN (Security - CC)                        │    │
│  ├─────────────────────────────────────────────────────────────┤    │
│  │  ┌────────────────────────────────────────────────────┐     │    │
│  │  │        CONTROL (CC6.1 - Access Controls)           │     │    │
│  │  ├────────────────────────────────────────────────────┤     │    │
│  │  │  ┌───────────────────────────────────────────┐     │     │    │
│  │  │  │   REQUIREMENT                             │     │     │    │
│  │  │  │   "Restrict access to authorized users"  │     │     │    │
│  │  │  ├───────────────────────────────────────────┤     │     │    │
│  │  │  │  EVIDENCE                                 │     │     │    │
│  │  │  │  ├── IAM Policy Export                    │     │     │    │
│  │  │  │  ├── MFA Screenshot                       │     │     │    │
│  │  │  │  └── Access Review Logs                   │     │     │    │
│  │  │  └───────────────────────────────────────────┘     │     │    │
│  │  └────────────────────────────────────────────────────┘     │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 3.4 Why This Hierarchy Matters for Your Design

| Hierarchy Level | Design Implication |
|-----------------|-------------------|
| **Framework** | Top-level entity with version tracking |
| **Domain** | Optional grouping layer for organization |
| **Control** | Core reusable entity (can map to multiple frameworks) |
| **Requirement** | Can be inline with control or separate table |
| **Evidence** | Attachable to controls (many-to-many relationship) |

**Key Design Decision:** Should domains be a separate entity or just a `category` field on controls? 
- For MVP: Use a `category` field on controls (simpler)
- For full system: Create a `domains` table for proper hierarchy

---

## 4. Common Patterns Across Frameworks

| Pattern | SOC 2 | PCI DSS | ISO 27001 |
|---------|-------|---------|-----------|
| **Hierarchy** | Criteria → Controls → Points of Focus | Goals → Requirements → Sub-requirements | Domains → Controls → Implementation guidance |
| **Access Control** | CC6.1-CC6.8 | Req 7, 8, 9 | A.5.15-A.5.18 |
| **Encryption** | CC6.1, C1.1 | Req 3, 4 | A.8.24 |
| **Logging & Monitoring** | CC7.2, CC7.3 | Req 10, 11 | A.8.15, A.8.16 |
| **Change Management** | CC8.1 | Req 6 | A.8.32 |
| **Incident Response** | CC7.4, CC7.5 | Req 12.10 | A.5.24-A.5.28 |
| **Risk Assessment** | CC3.1-CC3.4 | Req 12.2 | Clause 6.1 |

**Key Insight:** ~70% of controls overlap across frameworks. This is why **control reuse** is critical.

---

## 5. Evidence Types

| Evidence Type | Example | Used For |
|---------------|---------|----------|
| **Screenshots** | S3 encryption settings | Technical configs |
| **Exports/Logs** | Audit log exports | Monitoring controls |
| **Policies** | Acceptable Use Policy PDF | Organizational controls |
| **Certificates** | Training completion certificates | People controls |
| **Configuration Files** | Security group configs | Technical controls |
| **Attestations** | Signed acknowledgment forms | Manual verifications |

---

## 6. What Changes vs What Stays Stable

| Stable (Configuration) | Flexible (Runtime) |
|------------------------|-------------------|
| Framework definitions (SOC 2, PCI DSS) | Which company adopts which framework |
| Control templates and IDs | Which controls a company selects |
| Required evidence types | Actual evidence uploaded |
| Framework structure | Implementation details (frequency, owner) |
| Control descriptions | Notes, due dates, status |

**Key Insight:** This separation drives the **config-driven** architecture.

---

## 7. Versioning Considerations

Frameworks evolve over time:
- **PCI DSS:** v3.2.1 (2018) → v4.0 (2022)
- **ISO 27001:** 2013 → 2022 (reduced from 114 to 93 controls)
- **SOC 2:** Trust Services Criteria updated periodically

**Design Implication:** Must track:
- Framework version
- Control version
- Mapping between old and new controls during transitions

---

## 8. Key Terminology Glossary

| Term | Definition |
|------|------------|
| **Framework** | A compliance standard (SOC 2, PCI DSS, ISO 27001) |
| **Domain/Category** | A grouping within a framework (Security, Access Control) |
| **Control** | A specific security requirement |
| **Requirement** | A sub-item or specific aspect of a control |
| **Evidence** | Proof that a control is implemented |
| **Audit** | External verification of compliance |
| **Attestation** | Formal statement confirming compliance |
| **Gap** | A control that lacks sufficient evidence |
| **Readiness** | Percentage of controls with evidence |

---

## 9. Design Implications for Phase 1

Based on this research, your RMF engine design should address:

1. **Hierarchical Structure**
   - Frameworks contain domains/categories
   - Domains contain controls
   - Controls can have sub-requirements

2. **Many-to-Many Relationships**
   - One control can map to multiple frameworks
   - One evidence item can satisfy multiple controls

3. **Versioning Strategy**
   - Track framework versions
   - Support control version evolution
   - Handle migrations between versions

4. **Flexibility Levels**
   - Framework definitions = read-only config
   - Company adoptions = user-editable
   - Evidence = user-uploaded

5. **Status Tracking**
   - Per-control status (not started, in progress, complete)
   - Per-framework readiness percentage
   - Gap identification

---

## 10. Resources for Further Reading

| Resource | Link | Use For |
|----------|------|---------|
| SOC 2 Overview | [AICPA](https://www.aicpa.org/resources/article/what-is-soc-2) | Understanding Trust Services Criteria |
| PCI DSS Standard | [PCI SSC](https://www.pcisecuritystandards.org/document_library) | 12 Requirements structure |
| ISO 27001 Annex A | [ISO.org](https://www.iso.org/standard/27001) | Control categories |
| NIST RMF | [CSRC.NIST.gov](https://csrc.nist.gov/projects/risk-management) | Risk management process |
| Vanta SOC 2 Guide | [Vanta](https://www.vanta.com/products/soc-2) | Real-world implementation |
| Drata Framework Library | [Drata](https://www.drata.com/platform) | Multi-framework approach |

---

## 11. Summary: What You Learned

✅ Frameworks have a **hierarchical structure** (Framework → Domain → Control → Evidence)  
✅ **~70% of controls overlap** across frameworks — reuse is essential  
✅ **Evidence** is proof; it can satisfy multiple controls  
✅ **Versioning** is required — frameworks and controls evolve  
✅ **Config vs runtime separation** is key to extensibility  
✅ **Partial adoption** is common — companies don't implement all controls  

---

**Next Step:** Move to Phase 1 and design the domain model, database schema, and API surface.
