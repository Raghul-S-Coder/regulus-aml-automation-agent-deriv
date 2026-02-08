from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.organization import Organization


class OrganizationRepository:
    @staticmethod
    def create(db: Session, organization: Organization) -> Organization:
        db.add(organization)
        db.commit()
        db.refresh(organization)
        return organization

    @staticmethod
    def get_by_id(db: Session, organization_id: str) -> Organization | None:
        return db.query(Organization).filter(Organization.organization_id == organization_id).first()

    @staticmethod
    def list(db: Session, offset: int, limit: int) -> list[Organization]:
        return db.query(Organization).order_by(Organization.organization_id).offset(offset).limit(limit).all()

    @staticmethod
    def count(db: Session) -> int:
        return db.query(Organization).count()

    @staticmethod
    def update(db: Session, organization: Organization) -> Organization:
        db.add(organization)
        db.commit()
        db.refresh(organization)
        return organization

