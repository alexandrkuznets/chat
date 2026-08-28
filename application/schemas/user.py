from pydantic import BaseModel, validators
from datetime import datetime


class UserBaseSchema(BaseModel):
    username: str


class UserCreate(UserBaseSchema):
    password1: str
    password2: str


class UserResponse(UserBaseSchema):
    id: int
    created_at: datetime
