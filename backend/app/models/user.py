from sqlalchemy import Boolean, Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"
    USER = "user"

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.STAFF)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    created_members = relationship("Member", back_populates="created_by_user")
    created_groups = relationship("Group", back_populates="created_by_user")
    created_projects = relationship("Project", back_populates="created_by_user")
    contributions = relationship("Contribution", back_populates="created_by_user") 