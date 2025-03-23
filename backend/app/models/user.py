from sqlalchemy import Column, String, Enum, Boolean
from app.db.base_class import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"

class User(Base):
    name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.STAFF)
    is_active = Column(Boolean, default=True) 