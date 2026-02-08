from pydantic import BaseModel

from app.schemas.user import UserOut


class AuthLogin(BaseModel):
    username: str
    password: str


class AuthToken(BaseModel):
    token: str
    token_type: str = "bearer"
    expires_at: str
    user: UserOut
