from loguru import logger
from sqlalchemy.orm import Session

from app.exceptions.base_exception import ConflictException, NotFoundException, ValidationException
from app.exceptions.error_codes import (
    CASE_ALREADY_CLOSED,
    CASE_DOC_GEN_FAILED,
    CASE_INVALID_DECISION,
    CASE_NOT_FOUND,
)
from app.models.case_decision import CaseDecision
from app.repositories.account_repository import AccountRepository
from app.repositories.case_repository import CaseRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.case import CaseDecisionCreate
from app.services.sar_pdf_generator import generate_sar_pdf
from app.utils.datetime_utils import utc_now


class CaseService:
    @staticmethod
    def list_cases(db: Session, page: int, page_size: int, status: str | None = None) -> tuple[list, int]:
        offset = (page - 1) * page_size
        items = CaseRepository.list(db, offset=offset, limit=page_size, status=status)
        total = CaseRepository.count(db, status=status)
        return items, total

    @staticmethod
    def get_case(db: Session, case_id: str):
        case = CaseRepository.get_by_id(db, case_id)
        if not case:
            raise NotFoundException(CASE_NOT_FOUND, "Case not found")
        return case

    @staticmethod
    def get_documents(db: Session, case_id: str):
        case = CaseRepository.get_by_id(db, case_id)
        if not case:
            raise NotFoundException(CASE_NOT_FOUND, "Case not found")
        return CaseRepository.get_documents(db, case_id)

    @staticmethod
    def create_decision(db: Session, case_id: str, data: CaseDecisionCreate):
        case = CaseRepository.get_by_id(db, case_id)
        if not case:
            raise NotFoundException(CASE_NOT_FOUND, "Case not found")
        if case.case_status == "CLOSE":
            raise ConflictException(CASE_ALREADY_CLOSED, "Case already closed")
        if data.decision not in {"ACCEPT", "REJECT"}:
            raise ValidationException(CASE_INVALID_DECISION, "Invalid decision")

        if not case.assigned_to:
            case.assigned_to = data.decision_by
            case.assigned_date = utc_now()

        decision = CaseDecision(
            case_id=case_id,
            decision=data.decision,
            decision_by=data.decision_by,
            decision_reason=data.decision_reason,
            next_action=data.next_action or "close-case",
            decision_date=data.decision_date or utc_now(),
        )

        if data.decision == "ACCEPT":
            case.case_status = "ACCEPTED"
            CaseRepository.update_case(db, case)
        elif data.decision == "REJECT":
            case.case_status = "CLOSE"
            case.case_closed_date = utc_now()
            CaseRepository.update_case(db, case)

            # Only update the specific transaction linked to this case
            if case.transaction_id:
                txn = TransactionRepository.get_by_id(db, case.transaction_id)
                if txn and txn.transaction_status == "held":
                    txn.transaction_status = "completed"
                    TransactionRepository.update(db, txn)

                    account = AccountRepository.get_by_number(db, case.account_number)
                    if account:
                        if txn.transaction_type in {"deposit", "trade-sell"}:
                            account.balance_amount += txn.transaction_amount
                        else:
                            account.balance_amount -= txn.transaction_amount
                        AccountRepository.update(db, account)

        return CaseRepository.create_decision(db, decision)

    @staticmethod
    def generate_sar(db: Session, case_id: str) -> bytes:
        """Pull existing document content from DB and generate a PDF. No LLM calls."""
        case = CaseRepository.get_by_id(db, case_id)
        if not case:
            raise NotFoundException(CASE_NOT_FOUND, "Case not found")

        # Fetch the latest SAR document content already generated during case creation
        documents = CaseRepository.get_documents(db, case_id)
        document_content = ""
        for doc in documents:
            if doc.content_type == "sar_draft" and doc.content:
                document_content = doc.content
                break

        logger.info(f"[TRACE] CaseService | generate_sar | case_id={case_id} | doc_length={len(document_content)} chars")

        try:
            pdf_bytes = generate_sar_pdf(case, document_content)
        except Exception as exc:
            logger.error(f"[TRACE] CaseService | generate_sar PDF failed | {exc}")
            raise ValidationException(CASE_DOC_GEN_FAILED, f"SAR PDF generation failed: {exc}") from exc

        logger.info(f"[TRACE] CaseService | generate_sar | PDF generated | {len(pdf_bytes)} bytes")
        return pdf_bytes
