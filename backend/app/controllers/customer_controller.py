from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.common import StandardHeaders, paginated_response, success_response
from app.schemas.customer import CustomerCreate, CustomerOut, CustomerUpdate
from app.services.customer_service import CustomerService
from app.utils.datetime_utils import utc_now

router = APIRouter()


@router.post("/", response_model=dict)
def create_customer(
    payload: CustomerCreate,
    request: Request,
    _headers: StandardHeaders = Depends(),
    db: Session = Depends(get_db),
):
    customer = CustomerService.create_customer(db, payload)
    data = CustomerOut.model_validate(customer).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())


@router.get("/", response_model=dict)
def list_customers(
    request: Request,
    page: int = 1,
    page_size: int = 20,
    _headers: StandardHeaders = Depends(),
    db: Session = Depends(get_db),
):
    items, total = CustomerService.list_customers(db, page, page_size)
    data = [CustomerOut.model_validate(item).model_dump() for item in items]
    return paginated_response(data, total, page, page_size, request.state.request_id, utc_now().isoformat())


@router.get("/{customer_id}", response_model=dict)
def get_customer(
    customer_id: str,
    request: Request,
    _headers: StandardHeaders = Depends(),
    db: Session = Depends(get_db),
):
    customer = CustomerService.get_customer(db, customer_id)
    data = CustomerOut.model_validate(customer).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())


@router.put("/{customer_id}", response_model=dict)
def update_customer(
    customer_id: str,
    payload: CustomerUpdate,
    request: Request,
    _headers: StandardHeaders = Depends(),
    db: Session = Depends(get_db),
):
    customer = CustomerService.update_customer(db, customer_id, payload)
    data = CustomerOut.model_validate(customer).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())
