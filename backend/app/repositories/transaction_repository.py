from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.transaction import Transaction


class TransactionRepository:
    @staticmethod
    def create(db: Session, transaction: Transaction) -> Transaction:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction

    @staticmethod
    def get_by_id(db: Session, transaction_id: str) -> Transaction | None:
        return (
            db.query(Transaction)
            .filter(Transaction.transaction_id == transaction_id)
            .execution_options(populate_existing=True)
            .first()
        )

    @staticmethod
    def list(
        db: Session,
        offset: int,
        limit: int,
        account_number: str | None = None,
        transaction_type: str | None = None,
        transaction_status: str | None = None,
    ) -> list[Transaction]:
        query = db.query(Transaction)
        if account_number:
            query = query.filter(Transaction.account_number == account_number)
        if transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_type)
        if transaction_status:
            query = query.filter(Transaction.transaction_status == transaction_status)
        return query.order_by(Transaction.transaction_date.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def list_by_account_and_status(db: Session, account_number: str, status: str) -> list[Transaction]:
        return (
            db.query(Transaction)
            .filter(Transaction.account_number == account_number, Transaction.transaction_status == status)
            .order_by(Transaction.transaction_date.desc())
            .all()
        )

    @staticmethod
    def count(
        db: Session,
        account_number: str | None = None,
        transaction_type: str | None = None,
        transaction_status: str | None = None,
    ) -> int:
        query = db.query(Transaction)
        if account_number:
            query = query.filter(Transaction.account_number == account_number)
        if transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_type)
        if transaction_status:
            query = query.filter(Transaction.transaction_status == transaction_status)
        return query.count()

    @staticmethod
    def update(db: Session, transaction: Transaction) -> Transaction:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
