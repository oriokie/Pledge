from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_login_access_token(client: TestClient, test_user: dict) -> None:
    login_data = {
        "username": test_user["phone_number"],
        "password": test_user["password"],
    }
    r = client.post("/api/v1/auth/login", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"

def test_login_access_token_incorrect_password(client: TestClient, test_user: dict) -> None:
    login_data = {
        "username": test_user["phone_number"],
        "password": "incorrectpassword",
    }
    r = client.post("/api/v1/auth/login", data=login_data)
    assert r.status_code == 401
    assert "detail" in r.json()

def test_login_access_token_incorrect_username(client: TestClient) -> None:
    login_data = {
        "username": "nonexistent@example.com",
        "password": "testpassword123",
    }
    r = client.post("/api/v1/auth/login", data=login_data)
    assert r.status_code == 401
    assert "detail" in r.json()

def test_test_token(client: TestClient, test_user_token_headers: dict) -> None:
    r = client.post("/api/v1/auth/test-token", headers=test_user_token_headers)
    result = r.json()
    assert r.status_code == 200
    assert "phone_number" in result
    assert result["phone_number"] == test_user_token_headers["phone_number"]

def test_test_token_invalid_token(client: TestClient) -> None:
    headers = {"Authorization": "Bearer invalid_token"}
    r = client.post("/api/v1/auth/test-token", headers=headers)
    assert r.status_code == 401
    assert "detail" in r.json() 