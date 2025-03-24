from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum as PyEnum

class PledgeStatus(str, PyEnum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

class Pledge(Base):
    __tablename__ = "pledges"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    amount = Column(Numeric(10, 2))
    pledge_date = Column(Date)
    due_date = Column(Date)
    status = Column(String, default=PledgeStatus.PENDING)
    description = Column(Text, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    member = relationship("Member", back_populates="pledges")
    group = relationship("Group", back_populates="pledges")
    project = relationship("Project", back_populates="pledges")
    created_by_user = relationship("User", back_populates="pledges") 