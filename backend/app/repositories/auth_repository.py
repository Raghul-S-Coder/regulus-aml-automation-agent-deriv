from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.user import User


class AuthRepository:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()
