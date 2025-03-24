from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    email = Column(String, unique=True, nullable=True)
    member_code = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("users.id"))

    # Relationships
    created_by_user = relationship("User", back_populates="created_members")
    contributions = relationship("Contribution", back_populates="member")
    pledges = relationship("Pledge", back_populates="member")
    groups = relationship("Group", secondary="group_member", back_populates="members")
    sms_messages = relationship("SMS", back_populates="member")
    notifications = relationship("Notification", back_populates="member") 