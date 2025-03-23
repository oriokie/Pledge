from typing import Optional
from pydantic import BaseModel
from datetime import date
from app.models.contribution import ContributionType

class ContributionBase(BaseModel):
    member_id: int
    project_id: int
    group_id: Optional[int] = None
    amount: float
    type: ContributionType
    pledge_date: Optional[date] = None
    contribution_date: Optional[date] = None

class ContributionCreate(ContributionBase):
    pass

class ContributionUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[ContributionType] = None
    pledge_date: Optional[date] = None
    contribution_date: Optional[date] = None

class ContributionInDBBase(ContributionBase):
    id: int
    created_by: int
    updated_by: int

    class Config:
        from_attributes = True

class Contribution(ContributionInDBBase):
    pass

class ContributionInDB(ContributionInDBBase):
    pass 