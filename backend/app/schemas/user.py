from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    organization_id: str
    username: str
    full_name: str
    email: str
    user_type: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    organization_id: str | None = None
    username: str | None = None
    full_name: str | None = None
    email: str | None = None
    user_type: str | None = None
    is_active: bool | None = None
    password: str | None = None


class UserOut(UserBase):
    user_id: str
    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str

    model_config = {"from_attributes": True}
