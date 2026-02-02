# Product Owner (Backend) – Take-Home Assignment  
**Role Focus:** Compliance automation platforms for SMBs  
**Primary Domains:** SOC 2, PCI DSS, ISO 27001 (extensible to other RMFs)  
**Tech Stack:** FastAPI, PostgreSQL, RabbitMQ, Docker, AWS, Python  
**Target Level:** Senior Backend Engineer / Product Owner

---

## Overall Time Expectation (Explicit)

**Total:** ~10-12 hours  
- **~4 hours** – Reading & domain familiarization  (phase 0)
- **~4 hours** – Design + hands-on technical work  (phase 1)
- **~4 hours** – Design + hands-on technical work  (phase 2)

This split is **intentional**. You are not expected to know compliance frameworks upfront. We want to evaluate how quickly and effectively you can ramp up in an unfamiliar domain.

---

## Phase 0 — Reading & Domain Familiarization  
**Time:** ~4 hours  
**Deliverable:** None (inputs for later phases)

You are expected to **skim and understand structure**, not memorize standards.

### Required Reading (starting points)
- **SOC 2 overview (structure & intent)**  
  https://www.aicpa.org/resources/article/what-is-soc-2

- **PCI DSS standard structure**  
  https://www.pcisecuritystandards.org/document_library

- **ISO 27001 (Annex A – structure only)**  
  https://www.iso.org/standard/27001

- **NIST Risk Management Framework (conceptual grounding)**  
  https://csrc.nist.gov/projects/risk-management

### What You Should Extract
- How frameworks are organized (domains → controls → requirements)
- How evidence and testing are implied
- Common patterns across frameworks
- Where flexibility is needed vs where rigidity is acceptable

---

## Phase 1 — RMF Framework Design (Research → Abstraction)  
**Time:** 4 hours max  
**Output:** Design document (Markdown or PDF, **3–5 pages max**)

### Problem Statement
Design a **config-driven Risk Management Framework (RMF) engine** that can support:
- SOC 2  
- PCI DSS  
- ISO 27001  
- Future frameworks (e.g., HIPAA, CMMC)  

The system must require **minimal code changes** when adding or evolving frameworks.

### Mandatory Capabilities
- Control reuse across frameworks  
- Evidence reuse across controls and frameworks  
- Framework and control versioning  
- Partial framework adoption (subset of controls)  

### What to Produce

#### 1. Domain Model
- Key concepts: frameworks, controls, evidence, tests/validations
- Clear separation of:
  - **Configuration**
  - **Code**
- What is stable vs what is expected to change

#### 2. Logical Database Schema (PostgreSQL)
- Core tables and relationships (logical, not exhaustive)
- How new frameworks are added without schema rewrites
- How framework/control evolution is handled over time

#### 3. API Surface (FastAPI – conceptual)
- Key endpoints (names + responsibilities)
- How APIs remain stable while frameworks change

#### 4. Extensibility & Trade-offs (Required)
- At least **3 explicit design trade-offs**
- What you intentionally simplified or excluded
- Why those decisions make sense for an SMB-focused product

> No SQL DDL or OpenAPI specs required. This section evaluates **thinking quality**, not implementation depth.

---

## Phase 2 — Technical Judgment & AI-Assisted Engineering  
**Time:** 4 hours max  
**Output:** GitHub repository (or zip) + README

### Objective
Implement a **small vertical slice** of the system you designed.  
Keep it intentionally minimal and focused.

### Example Scope (pick one)
- Create a framework and associated controls via API  
- Attach evidence metadata to a control  
- Run a simple “readiness” or status query  

---

### Mandatory Technical Requirements

#### 1. Use the Stack
- FastAPI
- PostgreSQL
- Docker (even minimal)
- Async where appropriate

#### 2. AI Usage & Evaluation (Mandatory)
This role expects **active, critical use of AI coding assistants**.

Include a section titled **“AI Usage & Evaluation”** covering:

- **Which AI assistant(s) you used**
  - e.g., Claude, ChatGPT, Copilot, Cursor

- **Why you chose them**
  - Strengths
  - Weaknesses
  - Suitability for this task

- **Prompts Used**
  - Initial prompts
  - Refinement prompts
  - Constraints or rules you applied
  - Share verbatim or near-verbatim (redact secrets only)

- **Critical Evaluation**
  - At least one concrete example where:
    - AI output was incorrect, suboptimal, or over-engineered
    - You identified the issue
    - You fixed or redesigned it
  - Explain *why* the AI failed

- **Guardrails for Future Iterations**
  - Rules, prompts, or checks you would add
  - How you would prevent similar issues next time

> Treat the AI like a junior engineer: fast, useful, and frequently wrong.

---

#### 3. Production Readiness Awareness
Demonstrate awareness of:
- Configuration vs environment separation
- Migrations (can be stubbed or described)
- Error handling strategy
- Observability/logging approach (even if minimal)

#### 4. CI/CD Awareness
Add **or clearly describe** a GitHub Actions workflow that covers:
- Linting
- Testing
- Docker build

#### 5. Mentorship Simulation (Required)
Include in your README:
- One example **PR comment** you would leave on a junior engineer’s code
- One example **refactor request** and the rationale behind it

---

## Evaluation Criteria (Transparent)

### Strong Signals
- Starts from problem framing, not tables or endpoints
- Clear separation of domain model and implementation
- Config-driven thinking
- Healthy skepticism of AI-generated code
- Explicit trade-offs and simplifications
- Clear written communication
- Mentorship mindset

### Weak Signals
- Hard-coded framework logic
- Over-engineering “just in case”
- Blind trust in AI output
- No critique or refactoring of AI-generated code
- Treating compliance as static checklists

---

## What We Do *Not* Expect
- Deep prior cybersecurity expertise
- Feature completeness
- UI polish
- Perfect code

---

## Final Note
This role involves:
- Ambiguous problem spaces
- Rapid learning in unfamiliar domains
- Heavy use of AI tools with human judgment
- Mentoring 1–2 engineers