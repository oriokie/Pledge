from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ....core import security
from ....core.config import settings
from ....api import deps
from ....schemas.user import User, Token
from ....models.user import User as UserModel

router = APIRouter()

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    
    The username field should contain the user's phone number.
    The response includes:
    - access_token: JWT token for authentication
    - token_type: Type of token (always "bearer")
    
    Raises:
    - 401 Unauthorized: If phone number/password is incorrect or user is inactive
    """
    user = db.query(UserModel).filter(UserModel.phone == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone number or password"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )
    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone number or password"
        )
    
    access_token = security.create_access_token(
        subject=user.id, role=user.role
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/test-token", response_model=User)
def test_token(current_user: UserModel = Depends(deps.get_current_user)) -> Any:
    """
    Test access token.
    
    Returns the current user's information if the token is valid.
    
    Raises:
    - 401 Unauthorized: If the token is invalid or expired
    """
    return current_user 
    return current_user 