from collections.abc import Sequence

from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.alert import Alert
from app.models.customer import Customer
from app.models.high_risk_account import HighRiskAccount
from app.models.transaction import Transaction


def get_account(db: Session, account_number: str) -> Account | None:
    return db.query(Account).filter(Account.account_number == account_number).first()


def get_customer(db: Session, customer_id: str) -> Customer | None:
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()


def get_latest_transaction(db: Session, account_number: str) -> Transaction | None:
    return (
        db.query(Transaction)
        .filter(Transaction.account_number == account_number)
        .order_by(Transaction.transaction_date.desc())
        .first()
    )


def get_transaction_history(db: Session, account_number: str, limit: int = 50) -> Sequence[Transaction]:
    return (
        db.query(Transaction)
        .filter(Transaction.account_number == account_number)
        .order_by(Transaction.transaction_date.desc())
        .limit(limit)
        .all()
    )


def get_alerts(db: Session, account_number: str) -> Sequence[Alert]:
    return db.query(Alert).filter(Alert.account_number == account_number).order_by(Alert.triggered_date.desc()).all()


def get_high_risk_info(db: Session, account_number: str) -> HighRiskAccount | None:
    return db.query(HighRiskAccount).filter(HighRiskAccount.account_number == account_number).first()
