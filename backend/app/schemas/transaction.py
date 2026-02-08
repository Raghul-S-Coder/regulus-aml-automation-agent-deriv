from datetime import datetime

from pydantic import BaseModel


class TransactionBase(BaseModel):
    account_number: str
    transaction_amount: float
    transaction_currency: str
    transaction_date: datetime
    transaction_type: str
    purpose: str | None = None
    deposit_source_type: str | None = None
    deposit_source_value: str | None = None
    deposit_source_country: str | None = None


class TransactionCreate(BaseModel):
    account_number: str
    transaction_amount: float
    transaction_currency: str
    transaction_date: datetime | None = None
    transaction_type: str
    purpose: str | None = None
    deposit_source_type: str | None = None
    deposit_source_value: str | None = None
    deposit_source_country: str | None = None


class TransactionOut(TransactionBase):
    transaction_id: str
    transaction_status: str
    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str

    model_config = {"from_attributes": True}
