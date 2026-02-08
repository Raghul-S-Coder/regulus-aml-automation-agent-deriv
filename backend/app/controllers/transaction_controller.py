from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.common import StandardHeaders, paginated_response, success_response
from app.schemas.transaction import TransactionCreate, TransactionOut
from app.services.transaction_service import TransactionService
from app.utils.datetime_utils import utc_now
from app.dependencies.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=dict)
def create_transaction(
    payload: TransactionCreate,
    request: Request,
    _headers: StandardHeaders = Depends(),
    db: Session = Depends(get_db),
):
    transaction = TransactionService.create_transaction(db, payload)
    data = TransactionOut.model_validate(transaction).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())


@router.get("/", response_model=dict)
def list_transactions(
    request: Request,
    page: int = 1,
    page_size: int = 20,
    account_number: str | None = None,
    transaction_type: str | None = None,
    transaction_status: str | None = None,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items, total = TransactionService.list_transactions(
        db,
        page,
        page_size,
        account_number=account_number,
        transaction_type=transaction_type,
        transaction_status=transaction_status,
    )
    data = [TransactionOut.model_validate(item).model_dump() for item in items]
    return paginated_response(data, total, page, page_size, request.state.request_id, utc_now().isoformat())


@router.get("/account/{account_number}", response_model=dict)
def list_transactions_by_account(
    account_number: str,
    request: Request,
    page: int = 1,
    page_size: int = 20,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items, total = TransactionService.list_transactions_by_account(db, account_number, page, page_size)
    data = [TransactionOut.model_validate(item).model_dump() for item in items]
    return paginated_response(data, total, page, page_size, request.state.request_id, utc_now().isoformat())


@router.get("/{transaction_id}", response_model=dict)
def get_transaction(
    transaction_id: str,
    request: Request,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    transaction = TransactionService.get_transaction(db, transaction_id)
    data = TransactionOut.model_validate(transaction).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())
