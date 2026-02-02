from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.models.models import Framework, Control, FrameworkControl
from app.database import SyncSession
from migrations.seed.framework import frameworks
from migrations.seed.control import controls
from migrations.seed.frameworkcontrol import framework_controls
from rich.progress import track


def upsert_frameworks(session: Session):
    """Upsert frameworks - insert or update on conflict."""
    for framework in track(frameworks, description="Upserting frameworks..."):
        stmt = insert(Framework).values(**framework.model_dump())
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],  # Primary key
            set_={
                "code": stmt.excluded.code,
                "version": stmt.excluded.version,
                "name": stmt.excluded.name,
                "description": stmt.excluded.description,
                "status": stmt.excluded.status,
            }
        )
        session.execute(stmt)
    session.commit()
    print(f"Upserted {len(frameworks)} frameworks")


def upsert_controls(session: Session):
    """Upsert controls - insert or update on conflict."""
    for control in track(controls, description="Upserting controls..."):
        stmt = insert(Control).values(**control.model_dump())
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],  # Primary key
            set_={
                "code": stmt.excluded.code,
                "title": stmt.excluded.title,
                "description": stmt.excluded.description,
                "category": stmt.excluded.category,
                "control_type": stmt.excluded.control_type,
            }
        )
        session.execute(stmt)
    session.commit()
    print(f"Upserted {len(controls)} controls")


def upsert_framework_controls(session: Session):
    """Upsert framework controls - insert or update on conflict."""
    for fc in track(framework_controls, description="Upserting framework controls..."):
        stmt = insert(FrameworkControl).values(**fc.model_dump())
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],  # Primary key
            set_={
                "framework_id": stmt.excluded.framework_id,
                "control_id": stmt.excluded.control_id,
                "framework_control_code": stmt.excluded.framework_control_code,
                "is_required": stmt.excluded.is_required,
            }
        )
        session.execute(stmt)
    session.commit()
    print(f"Upserted {len(framework_controls)} framework controls")


if __name__ == "__main__":
    with SyncSession() as session:
        upsert_frameworks(session)
        upsert_controls(session)
        upsert_framework_controls(session)
        print("Seed data upsert complete!")