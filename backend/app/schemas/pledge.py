from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class PledgeBase(BaseModel):
    member_id: int
    group_id: Optional[int] = None
    project_id: int
    amount: float = Field(gt=0)
    pledge_date: date
    due_date: date
    status: str = "PENDING"
    description: Optional[str] = None

class PledgeCreate(PledgeBase):
    pass

class PledgeUpdate(BaseModel):
    member_id: Optional[int] = None
    group_id: Optional[int] = None
    project_id: Optional[int] = None
    amount: Optional[float] = Field(None, gt=0)
    pledge_date: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    description: Optional[str] = None

class Pledge(PledgeBase):
    id: int
    created_by_id: int
    created_at: date
    updated_at: Optional[date] = None
    member_name: str
    group_name: Optional[str] = None
    project_name: str

    class Config:
        from_attributes = True 