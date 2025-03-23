from typing import Optional, List
from pydantic import BaseModel, Field, constr
from datetime import datetime
from enum import Enum

class SMSType(str, Enum):
    PLEDGE_CONFIRMATION = "pledge_confirmation"
    CONTRIBUTION_CONFIRMATION = "contribution_confirmation"
    REMINDER = "reminder"
    ANNOUNCEMENT = "announcement"

class SMSBase(BaseModel):
    message: str
    phone_number: constr(pattern=r'^\+?1?\d{9,15}$')

class SMSRequest(SMSBase):
    pass

class SingleSMS(SMSBase):
    pass

class BulkSMS(BaseModel):
    message: str
    phone_numbers: List[constr(pattern=r'^\+?1?\d{9,15}$')]

class SMSResponse(SMSBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None

    class Config:
        from_attributes = True 