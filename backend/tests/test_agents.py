from app.agents.master_agent import MasterAgent
from app.models.account import Account
from app.models.alert import Alert
from app.models.customer import Customer
from app.models.transaction import Transaction
from app.repositories.case_repository import CaseRepository
from app.utils.datetime_utils import utc_now
from app.utils.id_generator import generate_id


def _seed_account_with_alert(db_session):
    customer = Customer(
        customer_id="CUST-AGENT-1",
        customer_type="individual",
        full_name="Agent User",
        date_of_birth="1990-01-01",
        nationality="US",
        residency_country="US",
        id_type="SSN",
        id_number="333-33-3333",
        phone="+1-555-0103",
        email="agent@example.com",
        address_line1="33 Agent St",
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
        account_number="ACC-AGENT-1",
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
    txn = Transaction(
        transaction_id=generate_id("TXN"),
        account_number=account.account_number,
        transaction_amount=50000.0,
        transaction_currency="USD",
        transaction_date=utc_now(),
        transaction_type="deposit",
        transaction_status="held",
        deposit_source_country="US",
    )
    alert = Alert(
        alert_id=generate_id("ALERT"),
        account_number=account.account_number,
        alert_type="High Deposit",
        severity="high",
        rule_id="RULE-01",
        description="test",
        triggered_date=utc_now(),
    )
    db_session.add_all([customer, account, txn, alert])
    db_session.commit()
    return alert.alert_id


def test_master_agent_creates_case(db_session):
    alert_id = _seed_account_with_alert(db_session)
    master = MasterAgent()
    case = master.run_for_alert(db_session, alert_id)

    fetched = CaseRepository.get_by_id(db_session, case.case_id)
    assert fetched is not None
