from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from .base import BaseSchema, TimestampSchema
from enum import Enum

class PaymentMethod(str, Enum):
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    MOBILE_MONEY = "mobile_money"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"

class ContributionBase(BaseSchema):
    member_id: int
    group_id: Optional[int] = None
    project_id: int
    amount: condecimal(max_digits=10, decimal_places=2)
    pledge_date: date
    contribution_date: Optional[date] = None
    payment_method: PaymentMethod
    description: Optional[str] = None

class ContributionCreate(ContributionBase):
    pass

class ContributionUpdate(BaseSchema):
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    contribution_date: Optional[date] = None
    payment_method: Optional[PaymentMethod] = None
    description: Optional[str] = None

class ContributionInDBBase(ContributionBase, TimestampSchema):
    id: int
    created_by_id: int

class Contribution(ContributionInDBBase):
    member_name: Optional[str] = None
    group_name: Optional[str] = None
    project_name: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ContributionSummary(BaseModel):
    total_amount: Decimal
    contribution_count: int
    member_count: int
    group_count: Optional[int]
    project_name: str
    start_date: date
    end_date: Optional[date] 