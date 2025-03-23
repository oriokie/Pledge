from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....core.security import get_password_hash
from ....api import deps
from ....schemas import user as user_schemas
from ....models.user import User, UserRole

router = APIRouter()

@router.get("/", response_model=List[user_schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve users. Staff can only see themselves, admins can see all users.
    """
    if current_user.role == UserRole.ADMIN:
        users = db.query(User).offset(skip).limit(limit).all()
    else:
        users = [current_user]
    return users

@router.post("/", response_model=user_schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: user_schemas.UserCreate,
    current_user: User = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Create new user. Only admins can create users.
    """
    user = db.query(User).filter(User.phone_number == user_in.phone_number).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this phone number already exists."
        )
    
    user = User(
        name=user_in.name,
        phone_number=user_in.phone_number,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        is_active=user_in.is_active
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.put("/{user_id}", response_model=user_schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: user_schemas.UserUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Update a user. Users can update their own data, admins can update any user.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own user data"
        )
    
    # Update user fields
    update_data = user_in.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", response_model=user_schemas.User)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: User = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Delete a user. Only admins can delete users.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Users cannot delete themselves"
        )
    
    db.delete(user)
    db.commit()
    return user 