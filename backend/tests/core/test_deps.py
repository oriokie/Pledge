import pytest
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.core.deps import (
    get_db,
    get_current_user,
    get_current_active_user,
    get_current_admin_user,
    get_current_staff_user
)
from app.models.user import User
from app.schemas.user import UserRole

@pytest.fixture
def mock_db():
    """Mock database session"""
    class MockDB:
        def __init__(self):
            self.committed = False
            self.rolled_back = False
        
        def commit(self):
            self.committed = True
        
        def rollback(self):
            self.rolled_back = True
    
    return MockDB()

@pytest.fixture
def test_user():
    """Create a test user"""
    return User(
        id=1,
        email="test@example.com",
        full_name="Test User",
        role=UserRole.STAFF,
        is_active=True
    )

def test_get_db(mock_db):
    """Test database dependency"""
    db = next(get_db())
    assert isinstance(db, Session)

def test_get_current_user(test_user, mock_db):
    """Test current user dependency"""
    # Create a valid token
    token = create_access_token({"sub": test_user.email})
    
    # Test valid token
    current_user = get_current_user(token, mock_db)
    assert current_user.email == test_user.email
    
    # Test invalid token
    with pytest.raises(HTTPException) as exc_info:
        get_current_user("invalid_token", mock_db)
    assert exc_info.value.status_code == 401

def test_get_current_active_user(test_user, mock_db):
    """Test active user dependency"""
    # Test active user
    token = create_access_token({"sub": test_user.email})
    current_user = get_current_active_user(get_current_user(token, mock_db))
    assert current_user.is_active is True
    
    # Test inactive user
    test_user.is_active = False
    with pytest.raises(HTTPException) as exc_info:
        get_current_active_user(test_user)
    assert exc_info.value.status_code == 400

def test_get_current_admin_user(test_user, mock_db):
    """Test admin user dependency"""
    # Test non-admin user
    with pytest.raises(HTTPException) as exc_info:
        get_current_admin_user(test_user)
    assert exc_info.value.status_code == 403
    
    # Test admin user
    test_user.role = UserRole.ADMIN
    admin_user = get_current_admin_user(test_user)
    assert admin_user.role == UserRole.ADMIN

def test_get_current_staff_user(test_user, mock_db):
    """Test staff user dependency"""
    # Test non-staff user
    test_user.role = UserRole.USER
    with pytest.raises(HTTPException) as exc_info:
        get_current_staff_user(test_user)
    assert exc_info.value.status_code == 403
    
    # Test staff user
    test_user.role = UserRole.STAFF
    staff_user = get_current_staff_user(test_user)
    assert staff_user.role == UserRole.STAFF
    
    # Test admin user (should also work)
    test_user.role = UserRole.ADMIN
    admin_user = get_current_staff_user(test_user)
    assert admin_user.role == UserRole.ADMIN 