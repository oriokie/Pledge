from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Member(Base):
    name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False, index=True)
    alias1 = Column(String)
    alias2 = Column(String)
    unique_code = Column(String(6), unique=True, nullable=False)
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_by = Column(Integer, ForeignKey("user.id"))
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])
    groups = relationship("GroupMember", back_populates="member")
    contributions = relationship("Contribution", back_populates="member") 