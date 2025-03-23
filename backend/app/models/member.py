from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Member(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, unique=True, index=True)
    alias1 = Column(String, nullable=True)
    alias2 = Column(String, nullable=True)
    unique_code = Column(String, unique=True, index=True)
    created_by_id = Column(Integer, ForeignKey("user.id"))
    
    # Relationships
    created_by_user = relationship("User", back_populates="created_members")
    groups = relationship("GroupMember", back_populates="member")
    contributions = relationship("Contribution", back_populates="member") 