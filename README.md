# RMF Compliance Engine

A config-driven Risk Management Framework (RMF) engine for compliance automation.

## Quick Start

```bash
# Start the application
docker-compose up -d

# Run migrations
docker-compose exec app alembic upgrade head

# Initialize seed data
docker-compose exec app python -m migrations.seed.gen_seed_data

# Create database for test cases
docker-compose exec db psql -U postgres -c "CREATE DATABASE compliance_test;"

# API is available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

## Project Structure

```
app/
├── __init__.py
├── main.py                  # FastAPI application entry point
├── config.py                # Configuration management
├── database.py              # Database connection and session
├── base.py                  # Base controller class
├── models/                  # SQLAlchemy models
│   ├── __init__.py
│   ├── models.py            # All model definitions
│   └── enums.py             # Enum types (FrameworkStatus, ControlCategory, etc.)
├── schemas/                 # Pydantic schemas
│   ├── __init__.py
│   ├── framework.py
│   ├── control.py
│   ├── organization.py
│   ├── evidence.py
│   └── readiness.py
├── api/                     # API layer
│   ├── __init__.py          # Router registration
│   ├── routes/              # Route definitions
│   │   ├── framework.py
│   │   ├── control.py
│   │   └── organization.py
│   └── controllers/         # Business logic
│       ├── frameworks.py
│       ├── control.py
│       └── organizations.py
└── helpers/                 # Shared utilities
    ├── __init__.py
    ├── common.py            # get_org_or_404, etc.
    └── readiness.py         # Readiness calculation logic

migrations/                  # Alembic migrations
├── versions/
│   ├── 000.py               # Create schemas (lookup, data, audit)
│   ├── 001_init.py          # Create all tables
│   ├── 002_*.py             # Schema updates
│   └── ...
├── seed/                    # Seed data scripts
│   ├── framework.py
│   ├── control.py
│   ├── frameworkcontrol.py
│   └── gen_seed_data.py     # Main seed runner
└── env.py

tests/                       # Test files
├── __init__.py
├── conftest.py              # Fixtures (db_session, seeded_db, client)
└── test_frameworks.py
```

## API Endpoints

### Frameworks (Read-Only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/frameworks` | List all frameworks (filter by `code`, `status`) |
| GET | `/frameworks/{id}` | Get framework details |
| GET | `/frameworks/{id}/controls` | List controls for a framework |

### Controls (Read-Only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/controls` | List all controls |
| GET | `/controls/{code}` | Get control details |

### Organizations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/organizations` | Create organization |
| GET | `/organizations/{slug}` | Get organization details |

### Framework Adoption
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/organizations/{slug}/frameworks` | Adopt a framework |
| GET | `/organizations/{slug}/frameworks` | List adopted frameworks |
| GET | `/organizations/{slug}/frameworks/{id}/controls` | List org's controls for a framework |

### Control Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| PATCH | `/organizations/{slug}/controls/{id}` | Update control status |

### Evidence
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/organizations/{slug}/evidence` | Create evidence metadata |
| GET | `/organizations/{slug}/evidence` | List all evidence |
| POST | `/organizations/{slug}/controls/{id}/evidence` | Link evidence to control |

### Readiness
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/organizations/{slug}/frameworks/{id}/readiness` | Get compliance readiness score |

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (without Docker)
uvicorn app.main:app --reload

# Run tests
pytest tests/ -v
```

---

## AI Usage & Evaluation

See [AI_PROMPTS.md](./AI_PROMPTS.md) for detailed prompt history and evaluation.

---

## Mentorship Simulation

### Example PR Comment

> **File:** `app/api/controllers/*`
> 
> **Comment:** Consider creating a helper function to organize response body.
> ```json
>{
>    "status": "success/failure",
>    "data": {}/[]
>    "message": ""
>}
> ```

> **Reason:** This will help in standardizing the response format across the application. It will also make it easier to add new fields in the future like pagination, etc. This will also help frontend developers to handle the response in a consistent way.

### Example Refactor Request

> **Current Code (database.py):**
> ```python
> # Engine created at module import time
> engine = create_async_engine(url)
> async_session = async_sessionmaker(engine)
> ```
> 
> **Problem:** Connection pool is created when Python imports the module, not when the app starts. This causes connection leaks during hot reload, makes testing harder, and doesn't clean up properly on shutdown.
> 
> **Requested Refactor:**
> ```python
> # database.py - Initialize in functions, not at import
> engine: AsyncEngine | None = None
> 
> async def init_db():
>     global engine
>     engine = create_async_engine(url)
> 
> async def close_db():
>     if engine:
>         await engine.dispose()
> 
> # main.py - Call in lifespan
> @asynccontextmanager
> async def lifespan(app: FastAPI):
>     await init_db()   # Pool created here
>     yield
>     await close_db()  # Pool disposed here
> ```
> 
> **Key Insight:** Pool = lifespan scope (once per app). Session = request scope (via `Depends(get_db)`).

---

## CI/CD Workflow

See [.github/workflows/ci.yml](.github/workflows/ci.yml) for the full workflow.

**Pipeline Steps:**
1. **Lint**: Run `ruff` and `black --check`
2. **Test**: Run `pytest` with PostgreSQL test container
3. **Build**: Build Docker image

### *Please refer to [design_document.md](./design_document.md) for detailed design and architecture decisions*
