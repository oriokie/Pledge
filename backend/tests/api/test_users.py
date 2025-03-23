import pytest
from fastapi import status
from app.schemas.user import UserRole, UserCreate, UserUpdate

def test_read_users_admin(client, admin_token_headers, test_user, test_staff):
    response = client.get("/api/v1/users/", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert len(users) >= 2
    assert any(user["phone_number"] == test_user["phone_number"] for user in users)
    assert any(user["phone_number"] == test_staff["phone_number"] for user in users)

def test_read_users_staff(client, staff_token_headers, test_staff):
    response = client.get("/api/v1/users/", headers=staff_token_headers)
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert len(users) == 1
    assert users[0]["phone_number"] == test_staff["phone_number"]

def test_read_users_unauthorized(client):
    response = client.get("/api/v1/users/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_user_admin(client, admin_token_headers):
    user_data = {
        "phone_number": "+254700000004",
        "password": "newpass123",
        "full_name": "New User",
        "role": UserRole.STAFF,
        "is_active": True
    }
    response = client.post("/api/v1/users/", headers=admin_token_headers, json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_user = response.json()
    assert created_user["phone_number"] == user_data["phone_number"]
    assert created_user["full_name"] == user_data["full_name"]
    assert created_user["role"] == user_data["role"]

def test_create_user_staff(client, staff_token_headers):
    user_data = {
        "phone_number": "+254700000005",
        "password": "newpass123",
        "full_name": "New User",
        "role": UserRole.STAFF,
        "is_active": True
    }
    response = client.post("/api/v1/users/", headers=staff_token_headers, json=user_data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_create_user_duplicate_phone(client, admin_token_headers, test_user):
    user_data = {
        "phone_number": test_user["phone_number"],
        "password": "newpass123",
        "full_name": "New User",
        "role": UserRole.STAFF,
        "is_active": True
    }
    response = client.post("/api/v1/users/", headers=admin_token_headers, json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_read_user_admin(client, admin_token_headers, test_user):
    response = client.get(f"/api/v1/users/{test_user['id']}", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    user = response.json()
    assert user["phone_number"] == test_user["phone_number"]

def test_read_user_staff_own(client, staff_token_headers, test_staff):
    response = client.get(f"/api/v1/users/{test_staff['id']}", headers=staff_token_headers)
    assert response.status_code == status.HTTP_200_OK
    user = response.json()
    assert user["phone_number"] == test_staff["phone_number"]

def test_read_user_staff_other(client, staff_token_headers, test_user):
    response = client.get(f"/api/v1/users/{test_user['id']}", headers=staff_token_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_read_user_nonexistent(client, admin_token_headers):
    response = client.get("/api/v1/users/999", headers=admin_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_user_admin(client, admin_token_headers, test_user):
    update_data = {
        "full_name": "Updated Name",
        "is_active": True
    }
    response = client.put(
        f"/api/v1/users/{test_user['id']}",
        headers=admin_token_headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    updated_user = response.json()
    assert updated_user["full_name"] == update_data["full_name"]

def test_update_user_staff_own(client, staff_token_headers, test_staff):
    update_data = {
        "full_name": "Updated Name",
        "is_active": True
    }
    response = client.put(
        f"/api/v1/users/{test_staff['id']}",
        headers=staff_token_headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    updated_user = response.json()
    assert updated_user["full_name"] == update_data["full_name"]

def test_update_user_staff_other(client, staff_token_headers, test_user):
    update_data = {
        "full_name": "Updated Name",
        "is_active": True
    }
    response = client.put(
        f"/api/v1/users/{test_user['id']}",
        headers=staff_token_headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_update_user_nonexistent(client, admin_token_headers):
    update_data = {
        "full_name": "Updated Name",
        "is_active": True
    }
    response = client.put(
        "/api/v1/users/999",
        headers=admin_token_headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_user_admin(client, admin_token_headers, test_user):
    response = client.delete(f"/api/v1/users/{test_user['id']}", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    deleted_user = response.json()
    assert deleted_user["phone_number"] == test_user["phone_number"]

def test_delete_user_staff(client, staff_token_headers, test_user):
    response = client.delete(f"/api/v1/users/{test_user['id']}", headers=staff_token_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_delete_user_self(client, admin_token_headers, test_user):
    response = client.delete(f"/api/v1/users/{test_user['id']}", headers=admin_token_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Cannot delete your own user account"

def test_delete_user_nonexistent(client, admin_token_headers):
    response = client.delete("/api/v1/users/999", headers=admin_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND 