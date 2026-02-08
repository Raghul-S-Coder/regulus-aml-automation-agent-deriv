from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.alert import AlertOut
from app.schemas.common import StandardHeaders, paginated_response, success_response
from app.dependencies.auth import get_current_user
from app.services.alert_service import AlertService
from app.utils.datetime_utils import utc_now

router = APIRouter()


@router.get("/", response_model=dict)
def list_alerts(
    request: Request,
    page: int = 1,
    page_size: int = 20,
    account_number: str | None = None,
    severity: str | None = None,
    rule_id: str | None = None,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items, total = AlertService.list_alerts(
        db,
        page,
        page_size,
        account_number=account_number,
        severity=severity,
        rule_id=rule_id,
    )
    data = [AlertOut.model_validate(item).model_dump() for item in items]
    return paginated_response(data, total, page, page_size, request.state.request_id, utc_now().isoformat())


@router.get("/account/{account_number}", response_model=dict)
def list_alerts_by_account(
    account_number: str,
    request: Request,
    page: int = 1,
    page_size: int = 20,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items, total = AlertService.list_alerts_by_account(db, account_number, page, page_size)
    data = [AlertOut.model_validate(item).model_dump() for item in items]
    return paginated_response(data, total, page, page_size, request.state.request_id, utc_now().isoformat())


@router.get("/{alert_id}", response_model=dict)
def get_alert(
    alert_id: str,
    request: Request,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    alert = AlertService.get_alert(db, alert_id)
    data = AlertOut.model_validate(alert).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())
