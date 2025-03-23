import pytest
from sqlalchemy.orm import Session
from app.core.db import SessionLocal, engine, Base
from app.models.user import User
from app.schemas.user import UserRole

@pytest.fixture(scope="function")
def db():
    """Create a fresh database session for each test"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    session = SessionLocal()
    
    try:
        yield session
    finally:
        # Clean up
        session.close()
        # Drop all tables
        Base.metadata.drop_all(bind=engine)

def test_db_session_creation(db):
    """Test database session creation"""
    assert isinstance(db, Session)
    assert db.is_active

def test_db_transaction_commit(db):
    """Test database transaction commit"""
    # Create a test user
    user = User(
        email="test@example.com",
        full_name="Test User",
        role=UserRole.STAFF,
        is_active=True
    )
    db.add(user)
    db.commit()
    
    # Verify user was saved
    saved_user = db.query(User).filter(User.email == "test@example.com").first()
    assert saved_user is not None
    assert saved_user.full_name == "Test User"

def test_db_transaction_rollback(db):
    """Test database transaction rollback"""
    # Create a test user
    user = User(
        email="test@example.com",
        full_name="Test User",
        role=UserRole.STAFF,
        is_active=True
    )
    db.add(user)
    db.rollback()
    
    # Verify user was not saved
    saved_user = db.query(User).filter(User.email == "test@example.com").first()
    assert saved_user is None

def test_db_session_cleanup(db):
    """Test database session cleanup"""
    # Create a test user
    user = User(
        email="test@example.com",
        full_name="Test User",
        role=UserRole.STAFF,
        is_active=True
    )
    db.add(user)
    db.commit()
    
    # Close session
    db.close()
    
    # Verify session is closed
    assert not db.is_active

def test_db_session_context_manager():
    """Test database session context manager"""
    with SessionLocal() as db:
        # Create a test user
        user = User(
            email="test@example.com",
            full_name="Test User",
            role=UserRole.STAFF,
            is_active=True
        )
        db.add(user)
        db.commit()
        
        # Verify user was saved
        saved_user = db.query(User).filter(User.email == "test@example.com").first()
        assert saved_user is not None
        assert saved_user.full_name == "Test User"
    
    # Verify session is closed
    assert not db.is_active

def test_db_session_isolation(db):
    """Test database session isolation"""
    # Create a test user in first session
    user1 = User(
        email="test1@example.com",
        full_name="Test User 1",
        role=UserRole.STAFF,
        is_active=True
    )
    db.add(user1)
    db.commit()
    
    # Create a new session
    with SessionLocal() as db2:
        # Create another user in second session
        user2 = User(
            email="test2@example.com",
            full_name="Test User 2",
            role=UserRole.STAFF,
            is_active=True
        )
        db2.add(user2)
        db2.commit()
        
        # Verify both users exist in second session
        users = db2.query(User).all()
        assert len(users) == 2
        assert any(u.email == "test1@example.com" for u in users)
        assert any(u.email == "test2@example.com" for u in users)
    
    # Verify both users exist in first session
    users = db.query(User).all()
    assert len(users) == 2
    assert any(u.email == "test1@example.com" for u in users)
    assert any(u.email == "test2@example.com" for u in users) 