from sqlalchemy import Column, String, Integer, ForeignKey, Date, Numeric, Enum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class ContributionType(str, enum.Enum):
    PLEDGE = "pledge"
    CONTRIBUTION = "contribution"

class Contribution(Base):
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("group.id"))
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(Enum(ContributionType), nullable=False)
    pledge_date = Column(Date)
    contribution_date = Column(Date)
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_by = Column(Integer, ForeignKey("user.id"))
    
    # Relationships
    member = relationship("Member", back_populates="contributions")
    group = relationship("Group", back_populates="contributions")
    project = relationship("Project", back_populates="contributions")
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by]) 