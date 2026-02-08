from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.auth import AuthLogin, AuthToken
from app.schemas.common import StandardHeaders, success_response
from app.schemas.user import UserOut
from app.services.auth_service import AuthService
from app.utils.datetime_utils import utc_now

router = APIRouter()


@router.post("/login", response_model=dict)
def login(
    payload: AuthLogin,
    request: Request,
    _headers: StandardHeaders = Depends(),
    db: Session = Depends(get_db),
):
    token, user, expires_at = AuthService.authenticate(db, payload.username, payload.password)
    data = AuthToken(token=token, user=UserOut.model_validate(user), expires_at=expires_at).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())
