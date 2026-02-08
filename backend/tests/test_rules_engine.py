from app.models.account import Account
from app.models.customer import Customer
from app.models.transaction import Transaction
from app.repositories.alert_repository import AlertRepository
from app.services.transaction_service import TransactionService
from app.schemas.transaction import TransactionCreate
from app.utils.datetime_utils import utc_now


def _seed_customer_account(db_session):
    customer = Customer(
        customer_id="CUST-RULE-1",
        customer_type="individual",
        full_name="Rule User",
        date_of_birth="1990-01-01",
        nationality="US",
        residency_country="US",
        id_type="SSN",
        id_number="222-22-2222",
        phone="+1-555-0102",
        email="rule@example.com",
        address_line1="22 Rule St",
        address_city="Austin",
        address_country="US",
        kyc_status="verified",
        kyc_verified_date="2025-01-01",
        kyc_expired_date=None,
        risk_rating="low",
        created_date=utc_now(),
        updated_date=utc_now(),
        created_by="test",
        updated_by="test",
    )
    account = Account(
        account_number="ACC-RULE-1",
        customer_id=customer.customer_id,
        account_type="trading",
        account_status="active",
        opened_date="2024-01-01",
        branch_code="AUS",
        balance_amount=1000.0,
        balance_currency="USD",
        created_date=utc_now(),
        updated_date=utc_now(),
        created_by="test",
        updated_by="test",
    )
    db_session.add(customer)
    db_session.add(account)
    db_session.commit()


def test_high_deposit_triggers_alert(db_session):
    _seed_customer_account(db_session)

    payload = TransactionCreate(
        account_number="ACC-RULE-1",
        transaction_amount=50000.0,
        transaction_currency="USD",
        transaction_type="deposit",
        transaction_date=utc_now(),
        deposit_source_country="US",
    )

    txn: Transaction = TransactionService.create_transaction(db_session, payload)
    assert txn.transaction_status == "held"

    alerts = AlertRepository.list(db_session, offset=0, limit=10, account_number="ACC-RULE-1")
    assert len(alerts) >= 1
