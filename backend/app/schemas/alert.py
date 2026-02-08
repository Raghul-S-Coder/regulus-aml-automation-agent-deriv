from datetime import datetime

from pydantic import BaseModel


class AlertOut(BaseModel):
    alert_id: str
    account_number: str
    transaction_id: str | None = None
    alert_type: str
    severity: str
    rule_id: str
    description: str
    triggered_date: datetime
    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str

    model_config = {"from_attributes": True}
