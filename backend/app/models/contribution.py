from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from .base import Base

class Contribution(Base):
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("member.id"))
    group_id = Column(Integer, ForeignKey("group.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("project.id"))
    amount = Column(Numeric(10, 2))
    pledge_date = Column(Date)
    contribution_date = Column(Date, nullable=True)
    created_by_id = Column(Integer, ForeignKey("user.id"))
    
    # Relationships
    member = relationship("Member", back_populates="contributions")
    group = relationship("Group", back_populates="contributions")
    project = relationship("Project", back_populates="contributions")
    created_by_user = relationship("User", back_populates="contributions") 