from pathlib import Path
import sys

# Ensure the backend package root is on sys.path when running this file directly.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.utils.datetime_utils import utc_now


def seed_organizations(db: Session) -> Organization:
    # Check if organization already exists
    existing = db.query(Organization).filter(Organization.organization_id == "ORG-0001").first()
    if existing:
        return existing

    org = Organization(
        organization_id="ORG-0001",
        name="Regulus Financial",
        country="US",
        status="active",
        created_date=utc_now(),
        updated_date=utc_now(),
        created_by="seed",
        updated_by="seed",
    )
    db.add(org)
    db.commit()
    db.refresh(org)
    return org
