from app.models.account import Account
from app.models.customer import Customer
from app.repositories.case_repository import CaseRepository
from app.repositories.transaction_repository import TransactionRepository
from app.utils.datetime_utils import utc_now


def _seed_customer_account(db_session):
    customer = Customer(
        customer_id="CUST-E2E-1",
        customer_type="individual",
        full_name="E2E User",
        date_of_birth="1990-01-01",
        nationality="US",
        residency_country="US",
        id_type="SSN",
        id_number="444-44-4444",
        phone="+1-555-0104",
        email="e2e@example.com",
        address_line1="44 E2E St",
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
        account_number="ACC-E2E-1",
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
    db_session.add_all([customer, account])
    db_session.commit()


def test_full_pipeline(client, standard_headers, db_session):
    _seed_customer_account(db_session)

    payload = {
        "account_number": "ACC-E2E-1",
        "transaction_amount": 50000.0,
        "transaction_currency": "USD",
        "transaction_type": "deposit",
        "transaction_date": utc_now().isoformat(),
        "deposit_source_country": "US",
    }
    create_resp = client.post("/api/v1/transactions/", json=payload, headers=standard_headers)
    assert create_resp.status_code == 200

    txn_id = create_resp.json()["data"]["transaction_id"]
    txn = TransactionRepository.get_by_id(db_session, txn_id)
    assert txn.transaction_status == "held"

    cases = CaseRepository.list(db_session, offset=0, limit=10)
    assert len(cases) >= 1
    case = cases[0]

    decision_payload = {
        "decision": "REJECT",
        "decision_by": "compliance_manager1",
        "decision_reason": "False positive",
    }
    decision_resp = client.post(
        f"/api/v1/cases/{case.case_id}/decisions",
        json=decision_payload,
        headers=standard_headers,
    )
    assert decision_resp.status_code == 200

    txn = TransactionRepository.get_by_id(db_session, txn_id)
    assert txn.transaction_status == "completed"
