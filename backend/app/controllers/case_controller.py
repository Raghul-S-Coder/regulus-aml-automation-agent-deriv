import io

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.case import CaseDecisionCreate, CaseDecisionOut, CaseDocumentOut, CaseListItem, CaseOut
from app.schemas.common import StandardHeaders, paginated_response, success_response
from app.dependencies.auth import get_current_user
from app.services.case_service import CaseService
from app.utils.datetime_utils import utc_now

router = APIRouter()


@router.get("/", response_model=dict)
def list_cases(
    request: Request,
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items, total = CaseService.list_cases(db, page, page_size, status=status)
    data = [CaseListItem.model_validate(item).model_dump() for item in items]
    return paginated_response(data, total, page, page_size, request.state.request_id, utc_now().isoformat())


@router.get("/{case_id}", response_model=dict)
def get_case(
    case_id: str,
    request: Request,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    case = CaseService.get_case(db, case_id)
    data = CaseOut.model_validate(case).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())


@router.get("/{case_id}/documents", response_model=dict)
def get_case_documents(
    case_id: str,
    request: Request,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    documents = CaseService.get_documents(db, case_id)
    data = [CaseDocumentOut.model_validate(doc).model_dump() for doc in documents]
    return success_response(data, request.state.request_id, utc_now().isoformat())


@router.post("/{case_id}/decisions", response_model=dict)
def create_case_decision(
    case_id: str,
    payload: CaseDecisionCreate,
    request: Request,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    decision = CaseService.create_decision(db, case_id, payload)
    data = CaseDecisionOut.model_validate(decision).model_dump()
    return success_response(data, request.state.request_id, utc_now().isoformat())


@router.post("/{case_id}/generate-sar")
def generate_sar(
    case_id: str,
    request: Request,
    _headers: StandardHeaders = Depends(),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pdf_bytes = CaseService.generate_sar(db, case_id)
    filename = f"SAR_{case_id}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
