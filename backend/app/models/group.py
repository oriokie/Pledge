from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# Association table for many-to-many relationship between Group and Member
group_member = Table(
    "group_member",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("group.id"), primary_key=True),
    Column("member_id", Integer, ForeignKey("member.id"), primary_key=True)
)

class Group(Base):
    name = Column(String, nullable=False)
    description = Column(String)
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_by = Column(Integer, ForeignKey("user.id"))
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])
    members = relationship("Member", secondary=group_member, backref="group_memberships")
    contributions = relationship("Contribution", back_populates="group") 