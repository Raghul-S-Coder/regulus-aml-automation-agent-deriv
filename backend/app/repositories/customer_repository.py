from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:
    @staticmethod
    def create(db: Session, customer: Customer) -> Customer:
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    @staticmethod
    def get_by_id(db: Session, customer_id: str) -> Customer | None:
        return db.query(Customer).filter(Customer.customer_id == customer_id).first()

    @staticmethod
    def list(db: Session, offset: int, limit: int) -> list[Customer]:
        return db.query(Customer).order_by(Customer.customer_id).offset(offset).limit(limit).all()

    @staticmethod
    def count(db: Session) -> int:
        return db.query(Customer).count()

    @staticmethod
    def update(db: Session, customer: Customer) -> Customer:
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer
