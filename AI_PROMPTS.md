# AI Usage & Evaluation

Documenting my experience using AI coding assistants during this project.

## Tools Used

- **Antigravity (Google)** - code editor and agent for code generation and refactoring
- **Claude (Anthropic)** - model for code generation and refactoring

---

### The Good Stuff

Antigravity's document-based workflow was particularly effective: the AI documents the task first for user review, then implements it in stages. This incremental approach ensures the user is fully aware of the implementation details throughout the build process. Paring it with Claude for more complex tasks was a good strategy.
Probably saved me 3-4 hours of typing.

### The Bad Stuff

Although Antigravity is a great tool for greenfield projects, it is not a good tool for existing projects. It can understand the requirements and generate the code accordingly. It can also understand the existing code and generate the code accordingly. But it is not a good tool for existing projects. It is a good tool for greenfield projects. 

---

## Prompts Used (Verbatim)

Here are actual prompts I used during development:

### Initial Setup
> "Explain this take-home assignment to me. What is the goal, what frameworks do I need to understand, and what makes a good submission?"

> "Design a domain model for a config-driven RMF engine that supports SOC 2, PCI DSS, and ISO 27001 with control reuse across frameworks"

### Database Design
> "For storing framework definitions, should I use YAML config files that sync to DB or direct database seed migrations?"

> "Create SQLAlchemy models for Framework, Control, and FrameworkControl with proper relationships. Use UUIDs for primary keys."

### Seed Data
> "Create seed data for 3 compliance frameworks (SOC 2, PCI DSS, ISO 27001) and map controls to them. Use Pydantic models for type safety."

> "I want to update the seed script to use upsert instead of insert. Running it multiple times should update existing records, not fail."

> "Add percentage progress tracking to the for loops in the seed script"

### API Development
> "Create FastAPI endpoints for organization framework adoption with proper async patterns"

> "How can I make Alembic track enum changes as well?"

### Refinement Prompts
> "Does current implementation look fine?" (after reviewing database.py)

> "What are the cons of creating a global connection at application startup?"

> "Refer @assignment.md and check the whole code and see if it is ready to submit. Don't miss anything. Check everything. Highlight anything that can be a red flag."

---

## Where I Had to Push Back

### 1. Over-normalized Database Design

First thing AI suggested for frameworks:

```
frameworks (id, code, name)
    ↓
framework_versions (id, framework_id, version, ...)
```

I asked: "Do we actually need a separate versions table for MVP?"

Answer: No. Simpler design:
```
frameworks (id, code, version, name, ...)
UNIQUE(code, version)
```

**Takeaway:** AI defaults to "textbook" designs. For an MVP, simpler is usually better.

### 2. Config Storage Approach

AI suggested YAML config files with a sync-to-database command. Classic pattern, but...we already have Alembic. Why add another config layer?

Went with seed migrations instead. One less thing to maintain.

### 3. Repetitive Helper Code

AI generated this pattern like 5 times across different endpoints:

```python
result = await db.execute(select(Org).where(Org.slug == slug))
org = result.scalar_one_or_none()
if not org:
    raise HTTPException(status_code=404, detail="Organization not found")
```

Had to extract it myself:
```python
org = await get_org_or_404(db, slug)
```

Not rocket science, but AI won't do it for you.

---

## Actual Bugs AI Introduced

### Bug #1: Wrong ID Types

AI used `int` for all IDs in Pydantic schemas even though my models use `UUID`.

```python
# What AI wrote
class FrameworkResponse(BaseModel):
    id: int  # wrong!
```

Had to go through every schema and fix them. Annoying.

**Why it happened:** AI doesn't actually read your other files. It pattern-matches from training data where `id: int` is common.

### Bug #2: Framework Code as Identifier

AI wrote:
```python
@router.get("/{code}")
async def get_framework(code: str):
    ...
```

Problem: `code` isn't unique! "SOC2" can have v2023 and v2024. The unique constraint is `(code, version)`.

**Why it happened:** AI saw `code` and assumed it was an identifier. Domain knowledge matters.

### Bug #3: Database Connection at Application Startup (Big One)

This was the worst. AI set up the database connection at application startup.

**Correct approach:**

Pool = once per app. Session = once per request. AI mixed these up. (Can be improved further)

---

## My Guardrails Going Forward

1. **Question normalized designs** - Especially for MVP, flatter is often better
2. **Check for copy-paste patterns** - If I see the same 3 lines twice, extract it
3. **Verify types manually** - AI doesn't cross-reference files well
4. **Review connection/resource management carefully** - Subtle bugs here are painful
5. **Don't trust domain assumptions** - AI doesn't know your business logic
