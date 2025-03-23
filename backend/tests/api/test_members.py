from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_create_member(client: TestClient, test_user_token_headers: dict) -> None:
    data = {
        "name": "Test Member",
        "phone_number": "1234567891",
        "alias": "TM",
        "is_active": True,
    }
    response = client.post("/api/v1/members/", headers=test_user_token_headers, json=data)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["phone_number"] == data["phone_number"]
    assert content["alias"] == data["alias"]
    assert content["is_active"] == data["is_active"]
    assert "unique_code" in content

def test_create_member_existing_phone(client: TestClient, test_user_token_headers: dict) -> None:
    # First create a member
    data = {
        "name": "Test Member",
        "phone_number": "1234567892",
        "alias": "TM",
        "is_active": True,
    }
    client.post("/api/v1/members/", headers=test_user_token_headers, json=data)
    
    # Try to create another member with the same phone number
    response = client.post("/api/v1/members/", headers=test_user_token_headers, json=data)
    assert response.status_code == 400
    assert "detail" in response.json()

def test_read_members(client: TestClient, test_user_token_headers: dict) -> None:
    response = client.get("/api/v1/members/", headers=test_user_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)

def test_read_member(client: TestClient, test_user_token_headers: dict) -> None:
    # First create a member
    data = {
        "name": "Test Member",
        "phone_number": "1234567893",
        "alias": "TM",
        "is_active": True,
    }
    create_response = client.post("/api/v1/members/", headers=test_user_token_headers, json=data)
    member_id = create_response.json()["id"]
    
    # Read the created member
    response = client.get(f"/api/v1/members/{member_id}", headers=test_user_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["phone_number"] == data["phone_number"]
    assert content["alias"] == data["alias"]
    assert content["is_active"] == data["is_active"]

def test_read_member_not_found(client: TestClient, test_user_token_headers: dict) -> None:
    response = client.get("/api/v1/members/999", headers=test_user_token_headers)
    assert response.status_code == 404
    assert "detail" in response.json()

def test_update_member(client: TestClient, test_user_token_headers: dict) -> None:
    # First create a member
    data = {
        "name": "Test Member",
        "phone_number": "1234567894",
        "alias": "TM",
        "is_active": True,
    }
    create_response = client.post("/api/v1/members/", headers=test_user_token_headers, json=data)
    member_id = create_response.json()["id"]
    
    # Update the member
    update_data = {
        "name": "Updated Member",
        "alias": "UM",
        "is_active": False,
    }
    response = client.put(
        f"/api/v1/members/{member_id}", headers=test_user_token_headers, json=update_data
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == update_data["name"]
    assert content["alias"] == update_data["alias"]
    assert content["is_active"] == update_data["is_active"]

def test_update_member_not_found(client: TestClient, test_user_token_headers: dict) -> None:
    update_data = {
        "name": "Updated Member",
        "alias": "UM",
        "is_active": False,
    }
    response = client.put("/api/v1/members/999", headers=test_user_token_headers, json=update_data)
    assert response.status_code == 404
    assert "detail" in response.json()

def test_delete_member(client: TestClient, test_admin_token_headers: dict) -> None:
    # First create a member
    data = {
        "name": "Test Member",
        "phone_number": "1234567895",
        "alias": "TM",
        "is_active": True,
    }
    create_response = client.post("/api/v1/members/", headers=test_admin_token_headers, json=data)
    member_id = create_response.json()["id"]
    
    # Delete the member
    response = client.delete(f"/api/v1/members/{member_id}", headers=test_admin_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["phone_number"] == data["phone_number"]
    assert content["alias"] == data["alias"]

def test_delete_member_not_found(client: TestClient, test_admin_token_headers: dict) -> None:
    response = client.delete("/api/v1/members/999", headers=test_admin_token_headers)
    assert response.status_code == 404
    assert "detail" in response.json()

def test_delete_member_unauthorized(client: TestClient, test_staff_token_headers: dict) -> None:
    # First create a member
    data = {
        "name": "Test Member",
        "phone_number": "1234567896",
        "alias": "TM",
        "is_active": True,
    }
    create_response = client.post("/api/v1/members/", headers=test_staff_token_headers, json=data)
    member_id = create_response.json()["id"]
    
    # Try to delete the member with staff token
    response = client.delete(f"/api/v1/members/{member_id}", headers=test_staff_token_headers)
    assert response.status_code == 403
    assert "detail" in response.json()

def test_read_member_by_code(client: TestClient, test_user_token_headers: dict) -> None:
    # First create a member
    data = {
        "name": "Test Member",
        "phone_number": "1234567897",
        "alias": "TM",
        "is_active": True,
    }
    create_response = client.post("/api/v1/members/", headers=test_user_token_headers, json=data)
    unique_code = create_response.json()["unique_code"]
    
    # Read the member by code
    response = client.get(f"/api/v1/members/code/{unique_code}", headers=test_user_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["phone_number"] == data["phone_number"]
    assert content["alias"] == data["alias"]
    assert content["unique_code"] == unique_code

def test_read_member_by_code_not_found(client: TestClient, test_user_token_headers: dict) -> None:
    response = client.get("/api/v1/members/code/999999", headers=test_user_token_headers)
    assert response.status_code == 404
    assert "detail" in response.json() 