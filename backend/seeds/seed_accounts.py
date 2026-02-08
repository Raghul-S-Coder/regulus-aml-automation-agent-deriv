from pathlib import Path
import sys

# Ensure the backend package root is on sys.path when running this file directly.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy.orm import Session

from app.models.account import Account
from app.utils.datetime_utils import utc_now


def seed_accounts(db: Session) -> list[Account]:
    # Check if accounts already exist
    existing_count = db.query(Account).filter(
        Account.account_number.in_(["ACC-000000001", "ACC-000000002", "ACC-000000003"])
    ).count()

    if existing_count >= 3:
        return db.query(Account).filter(
            Account.account_number.in_(["ACC-000000001", "ACC-000000002", "ACC-000000003"])
        ).all()

    # Delete any partial data to avoid conflicts
    db.query(Account).filter(
        Account.account_number.in_(["ACC-000000001", "ACC-000000002", "ACC-000000003"])
    ).delete(synchronize_session=False)
    db.commit()

    accounts = [
        Account(
            account_number="ACC-000000001",
            customer_id="CUST-000001",
            account_type="trading",
            account_status="active",
            opened_date="2024-01-10",
            branch_code="NYC",
            balance_amount=10000.0,
            balance_currency="USD",
            created_date=utc_now(),
            updated_date=utc_now(),
            created_by="seed",
            updated_by="seed",
        ),
        Account(
            account_number="ACC-000000002",
            customer_id="CUST-000002",
            account_type="trading",
            account_status="active",
            opened_date="2024-02-05",
            branch_code="DXB",
            balance_amount=8000.0,
            balance_currency="USD",
            created_date=utc_now(),
            updated_date=utc_now(),
            created_by="seed",
            updated_by="seed",
        ),
        Account(
            account_number="ACC-000000003",
            customer_id="CUST-000003",
            account_type="corporate",
            account_status="active",
            opened_date="2024-03-15",
            branch_code="SFO",
            balance_amount=50000.0,
            balance_currency="USD",
            created_date=utc_now(),
            updated_date=utc_now(),
            created_by="seed",
            updated_by="seed",
        ),
    ]
    db.add_all(accounts)
    db.commit()
    for a in accounts:
        db.refresh(a)
    return accounts
