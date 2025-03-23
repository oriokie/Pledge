import pytest
from fastapi import status
from app.schemas.user import UserRole

def test_login_success(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user["phone_number"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user["phone_number"],
            "password": "wrongpassword"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect phone number or password"

def test_login_nonexistent_user(client):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "+254700000999",
            "password": "testpass123"
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect phone number or password"

def test_login_inactive_user(client, db, test_user):
    # Deactivate user
    user = db.query(User).filter(User.id == test_user["id"]).first()
    user.is_active = False
    db.commit()
    
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user["phone_number"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Inactive user"

def test_test_token_success(client, admin_token_headers):
    response = client.post(
        "/api/v1/auth/test-token",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["phone_number"] == "+254700000000"
    assert response.json()["role"] == UserRole.ADMIN

def test_test_token_invalid_token(client):
    response = client.post(
        "/api/v1/auth/test-token",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Could not validate credentials"

def test_test_token_expired_token(client):
    # Create an expired token
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    response = client.post(
        "/api/v1/auth/test-token",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Could not validate credentials"

def test_test_token_missing_token(client):
    response = client.post("/api/v1/auth/test-token")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"

def test_test_token_wrong_token_type(client):
    response = client.post(
        "/api/v1/auth/test-token",
        headers={"Authorization": "Basic invalid_token"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated" 