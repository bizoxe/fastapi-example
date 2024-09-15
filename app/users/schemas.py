from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict, conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """ResponseUser"""

    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    """Used for response"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class UserLogin2(BaseModel):
    email: EmailStr
    password: str


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
