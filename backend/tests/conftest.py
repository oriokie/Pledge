import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User, UserRole

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="session")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture(scope="session")
def test_user(db):
    user = User(
        email="test@example.com",
        phone="+254700000001",
        full_name="Test User",
        hashed_password=get_password_hash("testpass123"),
        role=UserRole.MEMBER,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "id": user.id,
        "email": user.email,
        "phone": user.phone,
        "password": "testpass123",
        "role": user.role
    }

@pytest.fixture(scope="session")
def admin_user(db):
    user = User(
        email="admin@example.com",
        phone="+254700000000",
        full_name="Admin User",
        hashed_password=get_password_hash("adminpass123"),
        role=UserRole.ADMIN,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "id": user.id,
        "email": user.email,
        "phone": user.phone,
        "password": "adminpass123",
        "role": user.role
    }

@pytest.fixture(scope="session")
def staff_user(db):
    user = User(
        email="staff@example.com",
        phone="+254700000002",
        full_name="Staff User",
        hashed_password=get_password_hash("staffpass123"),
        role=UserRole.STAFF,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "id": user.id,
        "email": user.email,
        "phone": user.phone,
        "password": "staffpass123",
        "role": user.role
    }

@pytest.fixture(scope="session")
def admin_token_headers(client, admin_user):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": admin_user["phone"],
            "password": admin_user["password"]
        }
    )
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"} 