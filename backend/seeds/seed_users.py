from pathlib import Path
import sys

# Ensure the backend package root is on sys.path when running this file directly.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.datetime_utils import utc_now


def seed_users(db: Session, organization_id: str) -> list[User]:
    # Check if users already exist
    existing_admin = db.query(User).filter(User.user_id == "USR-0001").first()
    existing_cm = db.query(User).filter(User.user_id == "USR-0002").first()

    if existing_admin and existing_cm:
        return [existing_admin, existing_cm]

    users = []

    if not existing_admin:
        users.append(User(
            user_id="USR-0001",
            organization_id=organization_id,
            username="admin",
            password_hash="hashed_admin",
            full_name="Admin User",
            email="admin@regulus.local",
            user_type="admin",
            is_active=True,
            created_date=utc_now(),
            updated_date=utc_now(),
            created_by="seed",
            updated_by="seed",
        ))

    if not existing_cm:
        users.append(User(
            user_id="USR-0002",
            organization_id=organization_id,
            username="compliance_manager1",
            password_hash="hashed_cm1",
            full_name="Compliance Manager",
            email="cm1@regulus.local",
            user_type="compliance_manager",
            is_active=True,
            created_date=utc_now(),
            updated_date=utc_now(),
            created_by="seed",
            updated_by="seed",
        ))

    if users:
        db.add_all(users)
        db.commit()
        for u in users:
            db.refresh(u)

    return [existing_admin or users[0], existing_cm or users[-1]]
