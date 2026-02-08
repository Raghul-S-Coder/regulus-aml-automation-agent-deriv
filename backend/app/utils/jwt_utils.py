from datetime import UTC, datetime, timedelta

import jwt

from app.config.settings import settings


def create_access_token(subject: str) -> tuple[str, datetime]:
    expires_delta = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    expire = datetime.now(UTC) + expires_delta
    payload = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.now(UTC),
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token, expire


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
