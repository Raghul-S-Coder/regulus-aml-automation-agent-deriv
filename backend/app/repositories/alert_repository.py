from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.alert import Alert


class AlertRepository:
    @staticmethod
    def create(db: Session, alert: Alert) -> Alert:
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def get_by_id(db: Session, alert_id: str) -> Alert | None:
        return db.query(Alert).filter(Alert.alert_id == alert_id).first()

    @staticmethod
    def list(
        db: Session,
        offset: int,
        limit: int,
        account_number: str | None = None,
        severity: str | None = None,
        rule_id: str | None = None,
    ) -> list[Alert]:
        query = db.query(Alert)
        if account_number:
            query = query.filter(Alert.account_number == account_number)
        if severity:
            query = query.filter(Alert.severity == severity)
        if rule_id:
            query = query.filter(Alert.rule_id == rule_id)
        return query.order_by(Alert.triggered_date.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def count(
        db: Session,
        account_number: str | None = None,
        severity: str | None = None,
        rule_id: str | None = None,
    ) -> int:
        query = db.query(Alert)
        if account_number:
            query = query.filter(Alert.account_number == account_number)
        if severity:
            query = query.filter(Alert.severity == severity)
        if rule_id:
            query = query.filter(Alert.rule_id == rule_id)
        return query.count()
