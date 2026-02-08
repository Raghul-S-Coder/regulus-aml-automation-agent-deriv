from datetime import datetime

from pydantic import BaseModel


class AccountBase(BaseModel):
    customer_id: str
    account_type: str
    account_status: str
    opened_date: str
    branch_code: str
    balance_amount: float = 0.0
    balance_currency: str


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    account_type: str | None = None
    account_status: str | None = None
    opened_date: str | None = None
    branch_code: str | None = None
    balance_amount: float | None = None
    balance_currency: str | None = None


class AccountOut(AccountBase):
    account_number: str
    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str

    model_config = {"from_attributes": True}
