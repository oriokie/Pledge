from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, constr
from datetime import datetime
from .base import BaseSchema, TimestampSchema

class MemberBase(BaseModel):
    full_name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    alias1: Optional[str] = None
    alias2: Optional[str] = None
    is_active: bool = Field(default=True)

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    alias1: Optional[str] = None
    alias2: Optional[str] = None
    is_active: Optional[bool] = None

class Member(MemberBase):
    id: int
    member_code: str
    created_at: datetime
    updated_at: datetime
    created_by_id: int

    class Config:
        from_attributes = True

class MemberInDBBase(MemberBase, TimestampSchema):
    id: int
    member_code: str
    created_by_id: int

class Member(MemberInDBBase):
    total_contributions: Optional[float] = 0
    total_pledges: Optional[float] = 0
    group_names: Optional[List[str]] = []
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MemberSearchResult(BaseModel):
    id: int
    name: str
    unique_code: str
    matched_field: str  # Indicates which field matched the search (name, alias1, alias2, phone) 