import bcrypt
from sqlalchemy.orm import Session

from app.exceptions.base_exception import NotFoundException, ValidationException
from app.exceptions.error_codes import AUTH_INVALID_CREDENTIALS, USER_INACTIVE, USER_NOT_FOUND
from app.repositories.auth_repository import AuthRepository
from app.utils.jwt_utils import create_access_token


class AuthService:
    @staticmethod
    def authenticate(db: Session, username: str, password: str) -> tuple[str, object, str]:
        user = AuthRepository.get_user_by_username(db, username)
        if not user:
            raise NotFoundException(USER_NOT_FOUND, "User not found")
        if not user.is_active:
            raise ValidationException(USER_INACTIVE, "User is inactive")
        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            raise ValidationException(AUTH_INVALID_CREDENTIALS, "Invalid credentials")
        token, expires_at = create_access_token(user.user_id)
        return token, user, expires_at.isoformat()
