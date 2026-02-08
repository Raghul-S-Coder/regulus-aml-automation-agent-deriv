from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.account import Account


class AccountRepository:
    @staticmethod
    def create(db: Session, account: Account) -> Account:
        db.add(account)
        db.commit()
        db.refresh(account)
        return account

    @staticmethod
    def get_by_number(db: Session, account_number: str) -> Account | None:
        return db.query(Account).filter(Account.account_number == account_number).first()

    @staticmethod
    def list(db: Session, offset: int, limit: int) -> list[Account]:
        return db.query(Account).order_by(Account.account_number).offset(offset).limit(limit).all()

    @staticmethod
    def list_by_customer(db: Session, customer_id: str, offset: int, limit: int) -> list[Account]:
        return (
            db.query(Account)
            .filter(Account.customer_id == customer_id)
            .order_by(Account.account_number)
            .offset(offset)
            .limit(limit)
            .all()
        )

    @staticmethod
    def count(db: Session) -> int:
        return db.query(Account).count()

    @staticmethod
    def count_by_customer(db: Session, customer_id: str) -> int:
        return db.query(Account).filter(Account.customer_id == customer_id).count()

    @staticmethod
    def update(db: Session, account: Account) -> Account:
        db.add(account)
        db.commit()
        db.refresh(account)
        return account
