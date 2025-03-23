from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException
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
    OAuth2 compatible token login, get an access token for future requests
    """
    user = deps.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect phone number or password"
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
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
    Test access token
    """
    return current_user 