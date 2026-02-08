from datetime import timedelta
from pathlib import Path
import random
import sys

# Ensure the backend package root is on sys.path when running this file directly.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.case import Case
from app.models.transaction import Transaction
from app.utils.datetime_utils import utc_now
from app.utils.id_generator import generate_id


def seed_transactions(db: Session) -> list[Transaction]:
    # Check if transactions already exist
    existing_count = db.query(Transaction).count()
    if existing_count >= 100:
        return db.query(Transaction).limit(100).all()

    # Clear existing seed data to avoid conflicts
    db.query(Case).delete(synchronize_session=False)
    db.query(Alert).delete(synchronize_session=False)
    db.query(Transaction).delete(synchronize_session=False)
    db.commit()

    now = utc_now()
    random.seed(42)
    accounts = ["ACC-000000001", "ACC-000000002", "ACC-000000003"]
    rule_ids = ["RULE-01", "RULE-03", "RULE-05", "RULE-04"]
    txns: list[Transaction] = []
    alerts: list[Alert] = []
    cases: list[Case] = []

    for i in range(100):
        account_number = accounts[i % len(accounts)]
        rule_id = rule_ids[i % len(rule_ids)]
        amount = 10000.0 + (i * 137)  # above threshold to trigger alert
        tx_date = now - timedelta(hours=random.randint(0, 72), minutes=random.randint(0, 59))

        txn = Transaction(
            transaction_id=generate_id("TXN"),
            account_number=account_number,
            transaction_amount=amount,
            transaction_currency="USD",
            transaction_date=tx_date,
            transaction_type="deposit",
            transaction_status="held",
            deposit_source_country="US",
        )
        txns.append(txn)

        alert = Alert(
            alert_id=generate_id("ALERT"),
            account_number=account_number,
            transaction_id=txn.transaction_id,
            alert_type="rule",
            severity="high" if rule_id in {"RULE-01", "RULE-03"} else "medium",
            rule_id=rule_id,
            description=f"Seeded alert {rule_id} for {account_number}",
            triggered_date=tx_date,
        )
        alerts.append(alert)

        is_false_positive = i % 3 == 0
        case_score = 15.0 if is_false_positive else 78.0
        case = Case(
            case_id=generate_id("CASE"),
            alert_id=alert.alert_id,
            account_number=account_number,
            transaction_id=txn.transaction_id,
            case_status="OPEN",
            case_score_percentage=case_score,
            behavoir_agent_score=20.0 if is_false_positive else 80.0,
            behavoir_agent_summary="Seeded behavioral summary.",
            network_agent_score=18.0 if is_false_positive else 75.0,
            network_agent_summary="Seeded network summary.",
            contextual_agent_score=22.0 if is_false_positive else 82.0,
            contextual_agent_summary="Seeded contextual summary.",
            evidence_agent_score=19.0 if is_false_positive else 85.0,
            evidence_agent_summary="Seeded evidence summary.",
            false_positive_agent_score=90.0 if is_false_positive else 20.0,
            false_positive_agent_summary="Seeded false positive score.",
            assigned_to="compliance_manager",
            assigned_date=tx_date,
            case_opened_date=tx_date,
            case_summary="Seeded case record to avoid LLM calls.",
            created_date=tx_date,
            updated_date=tx_date,
            created_by="seed",
            updated_by="seed",
        )
        cases.append(case)
    db.add_all(txns)
    db.add_all(alerts)
    db.add_all(cases)
    db.commit()
    for t in txns:
        db.refresh(t)
    return txns
