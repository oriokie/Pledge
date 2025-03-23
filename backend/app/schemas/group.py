from pydantic import BaseModel
from typing import Optional, List
from .base import BaseSchema, TimestampSchema
from .member import Member

class GroupBase(BaseSchema):
    name: str

class GroupCreate(GroupBase):
    member_ids: Optional[List[int]] = []

class GroupUpdate(BaseSchema):
    name: Optional[str] = None
    member_ids: Optional[List[int]] = None

class GroupInDBBase(GroupBase, TimestampSchema):
    id: int
    created_by_id: int

class Group(GroupInDBBase):
    members: List[Member] = []
    total_contributions: Optional[float] = 0
    total_pledges: Optional[float] = 0

    class Config:
        from_attributes = True

class GroupWithStats(GroupBase):
    id: int
    member_count: int
    total_contributions: float
    total_pledges: float 