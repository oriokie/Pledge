from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
from enum import Enum

class SMSStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"

class SMS(Base):
    __tablename__ = "sms"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(SQLEnum(SMSStatus), default=SMSStatus.PENDING)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    sent_at = Column(DateTime, nullable=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=True)
    
    member = relationship("Member", back_populates="sms_messages") 