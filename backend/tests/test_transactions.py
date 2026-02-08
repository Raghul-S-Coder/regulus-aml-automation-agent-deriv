from app.models.account import Account
from app.models.customer import Customer
from app.models.transaction import Transaction
from app.utils.datetime_utils import utc_now


def _seed_customer_account(db_session):
    customer = Customer(
        customer_id="CUST-TXN-1",
        customer_type="individual",
        full_name="Txn User",
        date_of_birth="1990-01-01",
        nationality="US",
        residency_country="US",
        id_type="SSN",
        id_number="111-11-1111",
        phone="+1-555-0101",
        email="txn@example.com",
        address_line1="10 Txn St",
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
        account_number="ACC-TXN-1",
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


def test_create_transaction(client, standard_headers, db_session):
    _seed_customer_account(db_session)

    payload = {
        "account_number": "ACC-TXN-1",
        "transaction_amount": 100.0,
        "transaction_currency": "USD",
        "transaction_type": "deposit",
        "transaction_date": utc_now().isoformat(),
        "deposit_source_country": "US",
    }

    resp = client.post("/api/v1/transactions/", json=payload, headers=standard_headers)
    assert resp.status_code == 200
    data = resp.json()["data"]

    txn = db_session.query(Transaction).filter(Transaction.transaction_id == data["transaction_id"]).first()
    assert txn is not None
