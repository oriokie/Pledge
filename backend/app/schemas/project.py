from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import BaseSchema, TimestampSchema

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_amount: float = Field(gt=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str = "active"
    is_active: bool = True

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    target_amount: Optional[float] = Field(None, gt=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

class ProjectInDB(ProjectBase, TimestampSchema):
    id: int
    group_count: int = 0
    total_contributions: float = 0
    progress_percentage: float = 0

    class Config:
        from_attributes = True

class Project(ProjectBase):
    id: int
    group_count: int = 0
    total_contributions: float = 0
    progress_percentage: float = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProjectStats(BaseModel):
    id: int
    name: str
    total_contributions: float
    total_pledges: float
    contribution_count: int
    completion_percentage: float  # total_contributions / total_pledges * 100 