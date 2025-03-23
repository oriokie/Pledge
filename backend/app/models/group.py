from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .base import Base

# Association table for many-to-many relationship between groups and members
group_member = Table(
    'group_member',
    Base.metadata,
    Column('group_id', Integer, ForeignKey('group.id'), primary_key=True),
    Column('member_id', Integer, ForeignKey('member.id'), primary_key=True)
)

class Group(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_by_id = Column(Integer, ForeignKey("user.id"))
    
    # Relationships
    created_by_user = relationship("User", back_populates="created_groups")
    members = relationship("Member", secondary=group_member, backref="groups")
    contributions = relationship("Contribution", back_populates="group") 