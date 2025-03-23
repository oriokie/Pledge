from typing import Optional
from pydantic import BaseModel
from datetime import date

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    target_amount: Optional[float] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    target_amount: Optional[float] = None

class ProjectInDBBase(ProjectBase):
    id: int
    created_by: int
    updated_by: int

    class Config:
        from_attributes = True

class Project(ProjectInDBBase):
    pass

class ProjectInDB(ProjectInDBBase):
    pass 