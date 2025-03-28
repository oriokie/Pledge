from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.schemas.contribution import PaymentMethod

class Contribution(Base):
    __tablename__ = "contributions"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    amount = Column(Numeric(10, 2))
    pledge_date = Column(Date)
    contribution_date = Column(Date, nullable=True)
    payment_method = Column(Enum(PaymentMethod), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String, default="pending")
    error_message = Column(Text, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    member = relationship("Member", back_populates="contributions")
    group = relationship("Group", back_populates="contributions")
    project = relationship("Project", back_populates="contributions")
    created_by_user = relationship("User", back_populates="contributions") 