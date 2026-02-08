from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    @staticmethod
    def create(db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: str) -> User | None:
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def get_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def list(db: Session, offset: int, limit: int) -> list[User]:
        return db.query(User).order_by(User.user_id).offset(offset).limit(limit).all()

    @staticmethod
    def count(db: Session) -> int:
        return db.query(User).count()

    @staticmethod
    def update(db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
