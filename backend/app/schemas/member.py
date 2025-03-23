from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, constr
from datetime import datetime
from .base import BaseSchema, TimestampSchema

class MemberBase(BaseModel):
    email: EmailStr
    phone_number: constr(pattern=r'^\+?1?\d{9,15}$')
    first_name: str
    last_name: str
    role: str = Field(default="member")
    is_active: bool = Field(default=True)

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: Optional[constr(pattern=r'^\+?1?\d{9,15}$')] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class Member(MemberBase):
    id: int
    group_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MemberInDBBase(MemberBase, TimestampSchema):
    id: int
    created_by_id: int

class Member(MemberInDBBase):
    total_contributions: Optional[float] = 0
    total_pledges: Optional[float] = 0
    group_names: Optional[List[str]] = []

    class Config:
        from_attributes = True

class MemberSearchResult(BaseModel):
    id: int
    name: str
    unique_code: str
    matched_field: str  # Indicates which field matched the search (name, alias1, alias2, phone) 