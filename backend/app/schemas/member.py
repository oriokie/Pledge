from typing import Optional
from pydantic import BaseModel

class MemberBase(BaseModel):
    name: str
    phone_number: str
    alias1: Optional[str] = None
    alias2: Optional[str] = None

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    alias1: Optional[str] = None
    alias2: Optional[str] = None

class MemberInDBBase(MemberBase):
    id: int
    unique_code: str
    created_by: int
    updated_by: int

    class Config:
        from_attributes = True

class Member(MemberInDBBase):
    pass

class MemberInDB(MemberInDBBase):
    pass 