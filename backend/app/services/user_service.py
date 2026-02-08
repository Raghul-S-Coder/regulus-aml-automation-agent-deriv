import bcrypt
from sqlalchemy.orm import Session

from app.exceptions.base_exception import ConflictException, NotFoundException
from app.exceptions.error_codes import ORGANIZATION_NOT_FOUND, USER_DUPLICATE, USER_NOT_FOUND
from app.models.user import User
from app.repositories.organization_repository import OrganizationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.utils.id_generator import generate_id


class UserService:
    @staticmethod
    def create_user(db: Session, data: UserCreate) -> User:
        # Validate organization exists
        organization = OrganizationRepository.get_by_id(db, data.organization_id)
        if not organization:
            raise NotFoundException(ORGANIZATION_NOT_FOUND, f"Organization {data.organization_id} not found")

        existing = UserRepository.get_by_username(db, data.username)
        if existing:
            raise ConflictException(USER_DUPLICATE, "Username already exists")
        password_hash = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(
            user_id=generate_id("USR"),
            organization_id=data.organization_id,
            username=data.username,
            password_hash=password_hash,
            full_name=data.full_name,
            email=data.email,
            user_type=data.user_type,
            is_active=data.is_active,
        )
        return UserRepository.create(db, user)

    @staticmethod
    def list_users(db: Session, page: int, page_size: int) -> tuple[list[User], int]:
        offset = (page - 1) * page_size
        items = UserRepository.list(db, offset=offset, limit=page_size)
        total = UserRepository.count(db)
        return items, total

    @staticmethod
    def get_user(db: Session, user_id: str) -> User:
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise NotFoundException(USER_NOT_FOUND, "User not found")
        return user

    @staticmethod
    def update_user(db: Session, user_id: str, data: UserUpdate) -> User:
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise NotFoundException(USER_NOT_FOUND, "User not found")
        updates = data.model_dump(exclude_unset=True)
        if "username" in updates and updates["username"] != user.username:
            existing = UserRepository.get_by_username(db, updates["username"])
            if existing:
                raise ConflictException(USER_DUPLICATE, "Username already exists")
        if "password" in updates:
            password_hash = bcrypt.hashpw(
                updates["password"].encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            updates["password_hash"] = password_hash
            del updates["password"]
        for key, value in updates.items():
            setattr(user, key, value)
        return UserRepository.update(db, user)
