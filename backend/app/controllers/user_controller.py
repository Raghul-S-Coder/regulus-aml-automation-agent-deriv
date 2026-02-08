from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.common import StandardHeaders, paginated_response, success_response
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.user_service import UserService
from app.utils.datetime_utils import utc_now
from app.dependencies.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=dict)
def create_user(
    payload: UserCreate,
    request: Request,
    _headers: StandardHeaders = Depends(),
    db: Session = Depends(get_db),
):
    user = UserService.create_user(db, payload)
    data = UserOut.model_validate(user).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())


@router.get("/", response_model=dict)
def list_users(
    request: Request,
    page: int = 1,
    page_size: int = 20,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items, total = UserService.list_users(db, page, page_size)
    data = [UserOut.model_validate(item).model_dump() for item in items]
    return paginated_response(data, total, page, page_size, request.state.request_id, utc_now().isoformat())


@router.get("/{user_id}", response_model=dict)
def get_user(
    user_id: str,
    request: Request,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = UserService.get_user(db, user_id)
    data = UserOut.model_validate(user).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())


@router.put("/{user_id}", response_model=dict)
def update_user(
    user_id: str,
    payload: UserUpdate,
    request: Request,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = UserService.update_user(db, user_id, payload)
    data = UserOut.model_validate(user).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())
