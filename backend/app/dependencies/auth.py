from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.exceptions.base_exception import ValidationException
from app.exceptions.error_codes import AUTH_REQUIRED, AUTH_INSUFFICIENT_PERMISSIONS
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.jwt_utils import decode_access_token

auth_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or not credentials.credentials:
        raise ValidationException(AUTH_REQUIRED, "Authentication required")

    try:
        payload = decode_access_token(credentials.credentials)
    except Exception as exc:
        raise ValidationException(AUTH_REQUIRED, "Invalid or expired token") from exc

    user_id = payload.get("sub")
    if not user_id:
        raise ValidationException(AUTH_REQUIRED, "Invalid token payload")

    user = UserRepository.get_by_id(db, user_id)
    if not user:
        raise ValidationException(AUTH_REQUIRED, "User not found")
    if not user.is_active:
        raise ValidationException(AUTH_INSUFFICIENT_PERMISSIONS, "User inactive")
    return user
