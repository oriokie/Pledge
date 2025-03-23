from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.user import User
from ..core.security import get_password_hash, verify_password
from ..core.utils import validate_email, validate_phone_number
from ..schemas.user import UserCreate, UserUpdate

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(
        self,
        user_data: UserCreate
    ) -> Dict[str, Any]:
        """Create a new user."""
        try:
            # Validate email and phone number
            if not validate_email(user_data.email):
                return {"status": "error", "message": "Invalid email format"}
            
            if not validate_phone_number(user_data.phone_number):
                return {"status": "error", "message": "Invalid phone number format"}

            # Check if email already exists
            if self.db.query(User).filter(User.email == user_data.email).first():
                return {"status": "error", "message": "Email already registered"}

            # Create user
            user = User(
                email=user_data.email,
                full_name=user_data.full_name,
                phone_number=user_data.phone_number,
                hashed_password=get_password_hash(user_data.password),
                role=user_data.role,
                is_active=user_data.is_active
            )
            self.db.add(user)
            self.db.commit()

            return {
                "status": "success",
                "user_id": user.id,
                "message": "User created successfully"
            }
        except IntegrityError:
            return {"status": "error", "message": "User already exists"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_user_by_id(
        self,
        user_id: int
    ) -> Dict[str, Any]:
        """Get user by ID."""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"status": "error", "message": "User not found"}

            return {
                "status": "success",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "phone_number": user.phone_number,
                    "role": user.role,
                    "is_active": user.is_active,
                    "created_at": user.created_at.isoformat(),
                    "updated_at": user.updated_at.isoformat()
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_user_by_email(
        self,
        email: str
    ) -> Dict[str, Any]:
        """Get user by email."""
        try:
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                return {"status": "error", "message": "User not found"}

            return {
                "status": "success",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "phone_number": user.phone_number,
                    "role": user.role,
                    "is_active": user.is_active,
                    "created_at": user.created_at.isoformat(),
                    "updated_at": user.updated_at.isoformat()
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_user(
        self,
        user_id: int,
        user_data: UserUpdate
    ) -> Dict[str, Any]:
        """Update user information."""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"status": "error", "message": "User not found"}

            # Update fields if provided
            if user_data.email and user_data.email != user.email:
                if not validate_email(user_data.email):
                    return {"status": "error", "message": "Invalid email format"}
                if self.db.query(User).filter(User.email == user_data.email).first():
                    return {"status": "error", "message": "Email already registered"}
                user.email = user_data.email

            if user_data.full_name:
                user.full_name = user_data.full_name

            if user_data.phone_number and user_data.phone_number != user.phone_number:
                if not validate_phone_number(user_data.phone_number):
                    return {"status": "error", "message": "Invalid phone number format"}
                user.phone_number = user_data.phone_number

            if user_data.password:
                user.hashed_password = get_password_hash(user_data.password)

            if user_data.role:
                user.role = user_data.role

            if user_data.is_active is not None:
                user.is_active = user_data.is_active

            self.db.commit()

            return {
                "status": "success",
                "message": "User updated successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_user(
        self,
        user_id: int
    ) -> Dict[str, Any]:
        """Delete a user."""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"status": "error", "message": "User not found"}

            self.db.delete(user)
            self.db.commit()

            return {
                "status": "success",
                "message": "User deleted successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def authenticate_user(
        self,
        email: str,
        password: str
    ) -> Dict[str, Any]:
        """Authenticate a user."""
        try:
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                return {"status": "error", "message": "Invalid credentials"}

            if not verify_password(password, user.hashed_password):
                return {"status": "error", "message": "Invalid credentials"}

            if not user.is_active:
                return {"status": "error", "message": "User is inactive"}

            return {
                "status": "success",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        role: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Get list of users with optional filters."""
        try:
            query = self.db.query(User)

            if role:
                query = query.filter(User.role == role)
            if is_active is not None:
                query = query.filter(User.is_active == is_active)

            total_count = query.count()
            users = query.offset(skip).limit(limit).all()

            return {
                "status": "success",
                "total_count": total_count,
                "users": [
                    {
                        "id": user.id,
                        "email": user.email,
                        "full_name": user.full_name,
                        "phone_number": user.phone_number,
                        "role": user.role,
                        "is_active": user.is_active,
                        "created_at": user.created_at.isoformat(),
                        "updated_at": user.updated_at.isoformat()
                    }
                    for user in users
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)} 