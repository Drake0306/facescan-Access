from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.GUARD


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserInDB(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDB):
    pass
