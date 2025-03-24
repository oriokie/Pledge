from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLAlchemyEnum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime, UTC

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    contributions = relationship("Contribution", back_populates="created_by_user")
    sms_messages = relationship("SMS", back_populates="user")

    # Additional relationships
    created_members = relationship("Member", back_populates="created_by_user")
    created_groups = relationship("Group", back_populates="created_by_user")
    created_projects = relationship("Project", back_populates="created_by_user")
    pledges = relationship("Pledge", back_populates="created_by_user") 