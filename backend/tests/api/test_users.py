from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_create_user(client: TestClient, test_admin_token_headers: dict) -> None:
    data = {
        "phone_number": "newuser@example.com",
        "password": "newpassword123",
        "full_name": "New User",
        "is_active": True,
        "is_admin": False,
    }
    response = client.post("/api/v1/users/", headers=test_admin_token_headers, json=data)
    assert response.status_code == 200
    content = response.json()
    assert content["phone_number"] == data["phone_number"]
    assert content["full_name"] == data["full_name"]
    assert content["is_active"] == data["is_active"]
    assert content["is_admin"] == data["is_admin"]

def test_create_user_existing_phone(client: TestClient, test_admin_token_headers: dict, test_user: dict) -> None:
    data = {
        "phone_number": test_user["phone_number"],
        "password": "newpassword123",
        "full_name": "New User",
        "is_active": True,
        "is_admin": False,
    }
    response = client.post("/api/v1/users/", headers=test_admin_token_headers, json=data)
    assert response.status_code == 400
    assert "detail" in response.json()

def test_read_users(client: TestClient, test_admin_token_headers: dict) -> None:
    response = client.get("/api/v1/users/", headers=test_admin_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)

def test_read_users_unauthorized(client: TestClient, test_staff_token_headers: dict) -> None:
    response = client.get("/api/v1/users/", headers=test_staff_token_headers)
    assert response.status_code == 403
    assert "detail" in response.json()

def test_read_user_me(client: TestClient, test_user_token_headers: dict) -> None:
    response = client.get("/api/v1/users/me", headers=test_user_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert "phone_number" in content
    assert "full_name" in content

def test_read_user_by_id(client: TestClient, test_admin_token_headers: dict, test_user: dict) -> None:
    response = client.get(f"/api/v1/users/{test_user['id']}", headers=test_admin_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["phone_number"] == test_user["phone_number"]
    assert content["full_name"] == test_user["full_name"]

def test_read_user_by_id_not_found(client: TestClient, test_admin_token_headers: dict) -> None:
    response = client.get("/api/v1/users/999", headers=test_admin_token_headers)
    assert response.status_code == 404
    assert "detail" in response.json()

def test_update_user(client: TestClient, test_admin_token_headers: dict, test_user: dict) -> None:
    data = {
        "full_name": "Updated Name",
        "is_active": False,
    }
    response = client.put(
        f"/api/v1/users/{test_user['id']}", headers=test_admin_token_headers, json=data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["full_name"] == data["full_name"]
    assert content["is_active"] == data["is_active"]

def test_update_user_not_found(client: TestClient, test_admin_token_headers: dict) -> None:
    data = {
        "full_name": "Updated Name",
        "is_active": False,
    }
    response = client.put("/api/v1/users/999", headers=test_admin_token_headers, json=data)
    assert response.status_code == 404
    assert "detail" in response.json()

def test_delete_user(client: TestClient, test_admin_token_headers: dict, test_user: dict) -> None:
    response = client.delete(f"/api/v1/users/{test_user['id']}", headers=test_admin_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["phone_number"] == test_user["phone_number"]
    assert content["full_name"] == test_user["full_name"]

def test_delete_user_not_found(client: TestClient, test_admin_token_headers: dict) -> None:
    response = client.delete("/api/v1/users/999", headers=test_admin_token_headers)
    assert response.status_code == 404
    assert "detail" in response.json()

def test_delete_user_unauthorized(client: TestClient, test_staff_token_headers: dict, test_user: dict) -> None:
    response = client.delete(f"/api/v1/users/{test_user['id']}", headers=test_staff_token_headers)
    assert response.status_code == 403
    assert "detail" in response.json() 