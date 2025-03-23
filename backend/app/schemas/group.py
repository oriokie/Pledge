from typing import Optional, List
from pydantic import BaseModel
from app.schemas.member import Member

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    member_ids: Optional[List[int]] = None

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    member_ids: Optional[List[int]] = None

class GroupInDBBase(GroupBase):
    id: int
    created_by: int
    updated_by: int

    class Config:
        from_attributes = True

class Group(GroupInDBBase):
    members: List[Member] = []

class GroupInDB(GroupInDBBase):
    pass 