from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.case import Case
from app.models.case_decision import CaseDecision
from app.models.case_document_content import CaseDocumentContent


class CaseRepository:
    @staticmethod
    def create_case(db: Session, case: Case) -> Case:
        db.add(case)
        db.commit()
        db.refresh(case)
        return case

    @staticmethod
    def get_by_id(db: Session, case_id: str) -> Case | None:
        return db.query(Case).filter(Case.case_id == case_id).first()

    @staticmethod
    def list(db: Session, offset: int, limit: int, status: str | None = None) -> list[Case]:
        query = db.query(Case)
        if status:
            query = query.filter(Case.case_status == status)
        return query.order_by(Case.case_opened_date.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def count(db: Session, status: str | None = None) -> int:
        query = db.query(Case)
        if status:
            query = query.filter(Case.case_status == status)
        return query.count()

    @staticmethod
    def get_documents(db: Session, case_id: str) -> list[CaseDocumentContent]:
        return (
            db.query(CaseDocumentContent)
            .filter(CaseDocumentContent.case_id == case_id)
            .order_by(CaseDocumentContent.version.desc())
            .all()
        )

    @staticmethod
    def get_decisions(db: Session, case_id: str) -> list[CaseDecision]:
        return (
            db.query(CaseDecision)
            .filter(CaseDecision.case_id == case_id)
            .order_by(CaseDecision.decision_date.desc())
            .all()
        )

    @staticmethod
    def create_decision(db: Session, decision: CaseDecision) -> CaseDecision:
        db.add(decision)
        db.commit()
        db.refresh(decision)
        return decision

    @staticmethod
    def update_case(db: Session, case: Case) -> Case:
        db.add(case)
        db.commit()
        db.refresh(case)
        return case

    @staticmethod
    def create_document(db: Session, document: CaseDocumentContent) -> CaseDocumentContent:
        db.add(document)
        db.commit()
        db.refresh(document)
        return document
