from typing import Optional
from pydantic import BaseModel, Field, EmailStr, constr
from .base import BaseSchema, TimestampSchema
from ..models.user import UserRole
from datetime import datetime

class UserBase(BaseModel):
    """
    Base user schema with common attributes.
    
    Attributes:
        email: User's email address (optional)
        phone_number: User's phone number (optional)
        full_name: User's full name (optional)
        role: User's role (default: member)
        is_active: Whether the user account is active (default: true)
    """
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    full_name: Optional[str] = None
    role: UserRole = UserRole.STAFF
    is_active: bool = True

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    
    Extends UserBase with required fields.
    
    Attributes:
        email: User's email address (required)
        phone_number: User's phone number (required)
        full_name: User's full name (required)
        password: User's password (required)
    """
    email: EmailStr
    phone_number: str
    full_name: str
    password: str

class UserUpdate(UserBase):
    """
    Schema for updating an existing user.
    
    Extends UserBase with optional password field.
    
    Attributes:
        password: New password (optional)
    """
    password: Optional[str] = None

class UserInDBBase(UserBase):
    """
    Base schema for user data from database.
    
    Extends UserBase with database-specific fields.
    
    Attributes:
        id: User's unique identifier
        created_at: UTC timestamp of user creation
        updated_at: UTC timestamp of last update (optional)
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class User(UserInDBBase):
    """
    Schema for user data returned to clients.
    
    Extends UserInDBBase without additional fields.
    """
    pass

class UserInDB(UserInDBBase):
    """
    Schema for internal user data.
    
    Extends UserInDBBase with sensitive fields.
    
    Attributes:
        hashed_password: Hashed version of user's password
    """
    hashed_password: str

class Token(BaseModel):
    """
    Schema for authentication token.
    
    Attributes:
        access_token: JWT token string
        token_type: Type of token (default: "bearer")
    """
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """
    Schema for JWT token payload.
    
    Attributes:
        sub: User ID
        role: User's role
    """
    sub: int
    role: UserRole 