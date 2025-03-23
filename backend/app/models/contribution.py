from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from .base import Base

class Contribution(Base):
    __tablename__ = "contributions"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    amount = Column(Numeric(10, 2))
    pledge_date = Column(Date)
    contribution_date = Column(Date, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    member = relationship("Member", back_populates="contributions")
    group = relationship("Group", back_populates="contributions")
    project = relationship("Project", back_populates="contributions")
    created_by_user = relationship("User", back_populates="contributions") 