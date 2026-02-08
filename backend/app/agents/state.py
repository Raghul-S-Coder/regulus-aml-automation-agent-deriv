from typing import TypedDict


class AMLAnalysisState(TypedDict):
    alert_id: str
    account_number: str
    transaction_id: str

    customer_profile: dict
    account_info: dict
    transaction_history: list[dict]
    current_transaction: dict
    existing_alerts: list[dict]
    high_risk_info: dict | None

    behavioral_score: float
    behavioral_summary: str
    network_score: float
    network_summary: str
    contextual_score: float
    contextual_summary: str
    evidence_score: float
    evidence_summary: str
    false_positive_score: float
    false_positive_summary: str

    case_score_percentage: float
    case_classification: str
    case_summary: str
    document_content: str
