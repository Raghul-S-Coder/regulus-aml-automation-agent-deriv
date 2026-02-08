from datetime import datetime

from pydantic import BaseModel, Field


class CaseDecisionCreate(BaseModel):
    decision: str
    decision_by: str
    decision_reason: str
    next_action: str | None = None
    decision_date: datetime | None = None


class CaseDecisionOut(BaseModel):
    id: int
    case_id: str
    decision: str
    decision_by: str
    decision_date: datetime
    decision_reason: str
    next_action: str
    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str

    model_config = {"from_attributes": True}


class CaseDocumentOut(BaseModel):
    document_id: str
    case_id: str
    content_type: str
    content: str
    generated_by: str
    version: int
    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str

    model_config = {"from_attributes": True}


class CaseListItem(BaseModel):
    case_id: str
    alert_id: str
    account_number: str
    transaction_id: str | None = None
    case_status: str
    case_score_percentage: float
    assigned_to: str | None = None
    assigned_date: datetime | None = None
    case_opened_date: datetime
    case_closed_date: datetime | None = None
    case_summary: str
    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str

    model_config = {"from_attributes": True}


class CaseOut(BaseModel):
    case_id: str
    alert_id: str
    account_number: str
    transaction_id: str | None = None
    case_status: str
    case_score_percentage: float

    behavoir_agent_score: float | None = None
    behavoir_agent_summary: str | None = None
    network_agent_score: float | None = None
    network_agent_summary: str | None = None
    contextual_agent_score: float | None = None
    contextual_agent_summary: str | None = None
    evidence_agent_score: float | None = None
    evidence_agent_summary: str | None = None
    false_positive_agent_score: float | None = None
    false_positive_agent_summary: str | None = None

    assigned_to: str | None = None
    assigned_date: datetime | None = None
    case_opened_date: datetime
    case_closed_date: datetime | None = None
    case_summary: str

    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str

    documents: list[CaseDocumentOut] = Field(default_factory=list)
    decisions: list[CaseDecisionOut] = Field(default_factory=list)

    model_config = {"from_attributes": True}
