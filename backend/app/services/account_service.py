from sqlalchemy.orm import Session

from app.exceptions.base_exception import NotFoundException
from app.exceptions.error_codes import ACCOUNT_NOT_FOUND, CUSTOMER_NOT_FOUND
from app.models.account import Account
from app.models.customer import Customer
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountCreate, AccountUpdate
from app.utils.id_generator import generate_id


class AccountService:
    @staticmethod
    def create_account(db: Session, data: AccountCreate) -> Account:
        customer = db.query(Customer).filter(Customer.customer_id == data.customer_id).first()
        if not customer:
            raise NotFoundException(CUSTOMER_NOT_FOUND, "Customer not found")
        account = Account(
            account_number=generate_id("ACC"),
            **data.model_dump(),
        )
        return AccountRepository.create(db, account)

    @staticmethod
    def list_accounts(db: Session, page: int, page_size: int) -> tuple[list[Account], int]:
        offset = (page - 1) * page_size
        items = AccountRepository.list(db, offset=offset, limit=page_size)
        total = AccountRepository.count(db)
        return items, total

    @staticmethod
    def list_accounts_by_customer(
        db: Session, customer_id: str, page: int, page_size: int
    ) -> tuple[list[Account], int]:
        offset = (page - 1) * page_size
        items = AccountRepository.list_by_customer(db, customer_id, offset=offset, limit=page_size)
        total = AccountRepository.count_by_customer(db, customer_id)
        return items, total

    @staticmethod
    def get_account(db: Session, account_number: str) -> Account:
        account = AccountRepository.get_by_number(db, account_number)
        if not account:
            raise NotFoundException(ACCOUNT_NOT_FOUND, "Account not found")
        return account

    @staticmethod
    def update_account(db: Session, account_number: str, data: AccountUpdate) -> Account:
        account = AccountRepository.get_by_number(db, account_number)
        if not account:
            raise NotFoundException(ACCOUNT_NOT_FOUND, "Account not found")
        updates = data.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(account, key, value)
        return AccountRepository.update(db, account)
