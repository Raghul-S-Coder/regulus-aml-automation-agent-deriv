from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.account import AccountCreate, AccountOut, AccountUpdate
from app.schemas.common import StandardHeaders, paginated_response, success_response
from app.services.account_service import AccountService
from app.utils.datetime_utils import utc_now
from app.dependencies.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=dict)
def create_account(
    payload: AccountCreate,
    request: Request,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = AccountService.create_account(db, payload)
    data = AccountOut.model_validate(account).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())


@router.get("/", response_model=dict)
def list_accounts(
    request: Request,
    page: int = 1,
    page_size: int = 20,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items, total = AccountService.list_accounts(db, page, page_size)
    data = [AccountOut.model_validate(item).model_dump() for item in items]
    return paginated_response(data, total, page, page_size, request.state.request_id, utc_now().isoformat())


@router.get("/customer/{customer_id}", response_model=dict)
def list_accounts_by_customer(
    customer_id: str,
    request: Request,
    page: int = 1,
    page_size: int = 20,
    _headers: StandardHeaders = Depends(),
    db: Session = Depends(get_db),
):
    items, total = AccountService.list_accounts_by_customer(db, customer_id, page, page_size)
    data = [AccountOut.model_validate(item).model_dump() for item in items]
    return paginated_response(data, total, page, page_size, request.state.request_id, utc_now().isoformat())


@router.get("/{account_number}", response_model=dict)
def get_account(
    account_number: str,
    request: Request,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = AccountService.get_account(db, account_number)
    data = AccountOut.model_validate(account).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())


@router.put("/{account_number}", response_model=dict)
def update_account(
    account_number: str,
    payload: AccountUpdate,
    request: Request,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    account = AccountService.update_account(db, account_number, payload)
    data = AccountOut.model_validate(account).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())
