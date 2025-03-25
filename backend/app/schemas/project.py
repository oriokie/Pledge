from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal
from .base import BaseSchema, TimestampSchema

# Shared properties
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    target_amount: Decimal
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str = "active"
    is_active: bool = True

# Properties to receive on project creation
class ProjectCreate(ProjectBase):
    pass

# Properties to receive on project update
class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    target_amount: Optional[Decimal] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

# Properties shared by models stored in DB
class ProjectInDBBase(ProjectBase):
    id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Properties to return to client
class Project(ProjectInDBBase):
    pass

# Properties stored in DB
class ProjectInDB(ProjectInDBBase):
    group_count: int = 0
    total_contributions: float = 0
    progress_percentage: float = 0

class ProjectStats(BaseModel):
    id: int
    name: str
    total_contributions: Decimal
    total_pledges: Decimal
    contribution_count: int
    completion_percentage: Decimal 