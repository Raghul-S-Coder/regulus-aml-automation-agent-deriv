from pathlib import Path
import sys

# Ensure the backend package root is on sys.path when running this file directly.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.utils.datetime_utils import utc_now


def seed_customers(db: Session) -> list[Customer]:
    # Check if customers already exist
    existing_count = db.query(Customer).filter(
        Customer.customer_id.in_(["CUST-000001", "CUST-000002", "CUST-000003"])
    ).count()

    if existing_count >= 3:
        return db.query(Customer).filter(
            Customer.customer_id.in_(["CUST-000001", "CUST-000002", "CUST-000003"])
        ).all()

    # Delete any partial data to avoid conflicts
    db.query(Customer).filter(
        Customer.customer_id.in_(["CUST-000001", "CUST-000002", "CUST-000003"])
    ).delete(synchronize_session=False)
    db.commit()

    customers = [
        Customer(
            customer_id="CUST-000001",
            customer_type="individual",
            full_name="Alice Johnson",
            date_of_birth="1985-04-12",
            nationality="US",
            residency_country="US",
            id_type="SSN",
            id_number="123-45-6789",
            phone="+1-202-555-0111",
            email="alice@example.com",
            address_line1="123 Main St",
            address_city="New York",
            address_country="US",
            kyc_status="verified",
            kyc_verified_date="2025-01-01",
            kyc_expired_date=None,
            risk_rating="low",
            created_date=utc_now(),
            updated_date=utc_now(),
            created_by="seed",
            updated_by="seed",
        ),
        Customer(
            customer_id="CUST-000002",
            customer_type="individual",
            full_name="Bob Singh",
            date_of_birth="1978-09-30",
            nationality="IN",
            residency_country="AE",
            id_type="Passport",
            id_number="P1234567",
            phone="+971-50-555-0102",
            email="bob@example.com",
            address_line1="Sheikh Zayed Rd",
            address_city="Dubai",
            address_country="AE",
            kyc_status="verified",
            kyc_verified_date="2025-01-01",
            kyc_expired_date=None,
            risk_rating="medium",
            created_date=utc_now(),
            updated_date=utc_now(),
            created_by="seed",
            updated_by="seed",
        ),
        Customer(
            customer_id="CUST-000003",
            customer_type="corporate",
            full_name="Vega Trading LLC",
            date_of_birth="2005-06-01",
            nationality="US",
            residency_country="US",
            id_type="EIN",
            id_number="12-3456789",
            phone="+1-415-555-0199",
            email="ops@vega.example.com",
            address_line1="500 Market St",
            address_city="San Francisco",
            address_country="US",
            kyc_status="verified",
            kyc_verified_date="2025-01-01",
            kyc_expired_date=None,
            risk_rating="high",
            created_date=utc_now(),
            updated_date=utc_now(),
            created_by="seed",
            updated_by="seed",
        ),
    ]
    db.add_all(customers)
    db.commit()
    for c in customers:
        db.refresh(c)
    return customers
