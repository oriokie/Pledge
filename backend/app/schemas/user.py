from typing import Optional
from pydantic import BaseModel, Field, EmailStr, constr
from .base import BaseSchema, TimestampSchema
from ..models.user import UserRole
from datetime import datetime

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    full_name: Optional[str] = None
    role: UserRole = UserRole.MEMBER
    is_active: bool = True

class UserCreate(UserBase):
    email: EmailStr
    phone: str
    full_name: str
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: int
    role: UserRole 