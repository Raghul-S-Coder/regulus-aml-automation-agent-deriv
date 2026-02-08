from pathlib import Path
import sys

from loguru import logger

# Ensure the backend package root is on sys.path when running this file directly.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.config.database import SessionLocal, init_db
from seeds.seed_accounts import seed_accounts
from seeds.seed_customers import seed_customers
from seeds.seed_organizations import seed_organizations
from seeds.seed_transactions import seed_transactions
from seeds.seed_users import seed_users


def run() -> None:
    init_db()
    db = SessionLocal()
    try:
        org = seed_organizations(db)
        seed_users(db, org.organization_id)
        seed_customers(db)
        seed_accounts(db)
        seed_transactions(db)
        logger.info("Seed data inserted successfully")
    finally:
        db.close()


if __name__ == "__main__":
    run()
