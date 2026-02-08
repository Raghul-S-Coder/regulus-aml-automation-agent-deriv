from sqlalchemy.orm import Session

from app.exceptions.base_exception import NotFoundException
from app.exceptions.error_codes import CUSTOMER_NOT_FOUND
from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.utils.id_generator import generate_id


class CustomerService:
    @staticmethod
    def create_customer(db: Session, data: CustomerCreate) -> Customer:
        customer = Customer(
            customer_id=generate_id("CUST"),
            **data.model_dump(),
        )
        return CustomerRepository.create(db, customer)

    @staticmethod
    def list_customers(db: Session, page: int, page_size: int) -> tuple[list[Customer], int]:
        offset = (page - 1) * page_size
        items = CustomerRepository.list(db, offset=offset, limit=page_size)
        total = CustomerRepository.count(db)
        return items, total

    @staticmethod
    def get_customer(db: Session, customer_id: str) -> Customer:
        customer = CustomerRepository.get_by_id(db, customer_id)
        if not customer:
            raise NotFoundException(CUSTOMER_NOT_FOUND, "Customer not found")
        return customer

    @staticmethod
    def update_customer(db: Session, customer_id: str, data: CustomerUpdate) -> Customer:
        customer = CustomerRepository.get_by_id(db, customer_id)
        if not customer:
            raise NotFoundException(CUSTOMER_NOT_FOUND, "Customer not found")
        updates = data.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(customer, key, value)
        return CustomerRepository.update(db, customer)
