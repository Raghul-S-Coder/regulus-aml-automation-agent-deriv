from datetime import datetime

from pydantic import BaseModel


class CustomerBase(BaseModel):
    customer_type: str
    full_name: str
    date_of_birth: str
    nationality: str
    residency_country: str
    id_type: str
    id_number: str
    phone: str
    email: str
    address_line1: str
    address_city: str
    address_country: str
    kyc_status: str
    kyc_verified_date: str | None = None
    kyc_expired_date: str | None = None
    risk_rating: str


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    customer_type: str | None = None
    full_name: str | None = None
    date_of_birth: str | None = None
    nationality: str | None = None
    residency_country: str | None = None
    id_type: str | None = None
    id_number: str | None = None
    phone: str | None = None
    email: str | None = None
    address_line1: str | None = None
    address_city: str | None = None
    address_country: str | None = None
    kyc_status: str | None = None
    kyc_verified_date: str | None = None
    kyc_expired_date: str | None = None
    risk_rating: str | None = None


class CustomerOut(CustomerBase):
    customer_id: str
    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str

    model_config = {"from_attributes": True}
