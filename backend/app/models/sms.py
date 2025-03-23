from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class SMSStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"

class SMS(Base):
    __tablename__ = "sms"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text)
    recipient = Column(String)
    status = Column(SQLAlchemyEnum(SMSStatus), default=SMSStatus.PENDING)
    message_id = Column(String, unique=True)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    member_id = Column(Integer, ForeignKey("members.id"))

    # Relationships
    user = relationship("User", back_populates="sms_messages")
    member = relationship("Member", back_populates="sms_messages") 