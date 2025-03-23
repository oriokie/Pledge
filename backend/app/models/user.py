from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.database import Base

class UserRole(str, Enum):
    ADMIN = "admin"
    STAFF = "staff"
    MEMBER = "member"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.MEMBER)
    is_active = Column(Boolean, default=True)

    # Relationships
    contributions = relationship("Contribution", back_populates="created_by_user")
    sms_messages = relationship("SMS", back_populates="user")

    # Additional relationships
    created_members = relationship("Member", back_populates="created_by_user")
    created_groups = relationship("Group", back_populates="created_by_user")
    created_projects = relationship("Project", back_populates="created_by_user") 