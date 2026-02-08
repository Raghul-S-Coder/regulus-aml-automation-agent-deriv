from sqlalchemy.orm import Session

from app.exceptions.base_exception import NotFoundException
from app.exceptions.error_codes import ALERT_NOT_FOUND
from app.models.alert import Alert
from app.repositories.alert_repository import AlertRepository


class AlertService:
    @staticmethod
    def list_alerts(
        db: Session,
        page: int,
        page_size: int,
        account_number: str | None = None,
        severity: str | None = None,
        rule_id: str | None = None,
    ) -> tuple[list[Alert], int]:
        offset = (page - 1) * page_size
        items = AlertRepository.list(
            db,
            offset=offset,
            limit=page_size,
            account_number=account_number,
            severity=severity,
            rule_id=rule_id,
        )
        total = AlertRepository.count(
            db,
            account_number=account_number,
            severity=severity,
            rule_id=rule_id,
        )
        return items, total

    @staticmethod
    def list_alerts_by_account(db: Session, account_number: str, page: int, page_size: int) -> tuple[list[Alert], int]:
        return AlertService.list_alerts(db, page, page_size, account_number=account_number)

    @staticmethod
    def get_alert(db: Session, alert_id: str) -> Alert:
        alert = AlertRepository.get_by_id(db, alert_id)
        if not alert:
            raise NotFoundException(ALERT_NOT_FOUND, "Alert not found")
        return alert
