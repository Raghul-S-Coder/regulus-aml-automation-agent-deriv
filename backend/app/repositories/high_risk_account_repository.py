from sqlalchemy.orm import Session

from app.models.high_risk_account import HighRiskAccount


class HighRiskAccountRepository:
    @staticmethod
    def get_by_account(db: Session, account_number: str) -> HighRiskAccount | None:
        return db.query(HighRiskAccount).filter(HighRiskAccount.account_number == account_number).first()

    @staticmethod
    def create(db: Session, high_risk_account: HighRiskAccount) -> HighRiskAccount:
        db.add(high_risk_account)
        db.commit()
        db.refresh(high_risk_account)
        return high_risk_account

    @staticmethod
    def update(db: Session, high_risk_account: HighRiskAccount) -> HighRiskAccount:
        db.add(high_risk_account)
        db.commit()
        db.refresh(high_risk_account)
        return high_risk_account
