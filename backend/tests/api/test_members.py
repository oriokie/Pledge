import pytest
from fastapi import status
from app.schemas.member import MemberCreate, MemberUpdate

def test_read_members(client, admin_token_headers, test_member):
    response = client.get("/api/v1/members/", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    members = response.json()
    assert len(members) >= 1
    assert any(member["phone_number"] == test_member["phone_number"] for member in members)

def test_read_members_unauthorized(client):
    response = client.get("/api/v1/members/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_member(client, admin_token_headers):
    member_data = {
        "name": "New Member",
        "alias": "NM",
        "phone_number": "+254700000006"
    }
    response = client.post("/api/v1/members/", headers=admin_token_headers, json=member_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_member = response.json()
    assert created_member["name"] == member_data["name"]
    assert created_member["phone_number"] == member_data["phone_number"]
    assert created_member["unique_code"] is not None
    assert len(created_member["unique_code"]) == 6

def test_create_member_duplicate_phone(client, admin_token_headers, test_member):
    member_data = {
        "name": "Duplicate Member",
        "alias": "DM",
        "phone_number": test_member["phone_number"]
    }
    response = client.post("/api/v1/members/", headers=admin_token_headers, json=member_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_search_members_by_name(client, admin_token_headers, test_member):
    response = client.get(
        f"/api/v1/members/search?query={test_member['name']}",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    members = response.json()
    assert len(members) >= 1
    assert any(member["name"] == test_member["name"] for member in members)

def test_search_members_by_phone(client, admin_token_headers, test_member):
    response = client.get(
        f"/api/v1/members/search?query={test_member['phone_number']}",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    members = response.json()
    assert len(members) >= 1
    assert any(member["phone_number"] == test_member["phone_number"] for member in members)

def test_search_members_by_code(client, admin_token_headers, test_member):
    response = client.get(
        f"/api/v1/members/search?query={test_member['unique_code']}",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    members = response.json()
    assert len(members) >= 1
    assert any(member["unique_code"] == test_member["unique_code"] for member in members)

def test_search_members_empty_query(client, admin_token_headers):
    response = client.get("/api/v1/members/search?query=", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    members = response.json()
    assert len(members) == 0

def test_read_member(client, admin_token_headers, test_member):
    response = client.get(f"/api/v1/members/{test_member['id']}", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    member = response.json()
    assert member["phone_number"] == test_member["phone_number"]
    assert member["name"] == test_member["name"]

def test_read_member_nonexistent(client, admin_token_headers):
    response = client.get("/api/v1/members/999", headers=admin_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_member(client, admin_token_headers, test_member):
    update_data = {
        "name": "Updated Name",
        "alias": "UN"
    }
    response = client.put(
        f"/api/v1/members/{test_member['id']}",
        headers=admin_token_headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    updated_member = response.json()
    assert updated_member["name"] == update_data["name"]
    assert updated_member["alias"] == update_data["alias"]

def test_update_member_duplicate_phone(client, admin_token_headers, test_member, db):
    # Create another member
    other_member = Member(
        name="Other Member",
        alias="OM",
        phone_number="+254700000007",
        unique_code="OM001"
    )
    db.add(other_member)
    db.commit()
    
    update_data = {
        "phone_number": other_member.phone_number
    }
    response = client.put(
        f"/api/v1/members/{test_member['id']}",
        headers=admin_token_headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_update_member_nonexistent(client, admin_token_headers):
    update_data = {
        "name": "Updated Name",
        "alias": "UN"
    }
    response = client.put(
        "/api/v1/members/999",
        headers=admin_token_headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_member(client, admin_token_headers, test_member):
    response = client.delete(f"/api/v1/members/{test_member['id']}", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    deleted_member = response.json()
    assert deleted_member["phone_number"] == test_member["phone_number"]

def test_delete_member_nonexistent(client, admin_token_headers):
    response = client.delete("/api/v1/members/999", headers=admin_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_member_with_contributions(client, admin_token_headers, test_member, test_contribution):
    response = client.delete(f"/api/v1/members/{test_member['id']}", headers=admin_token_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Cannot delete member with existing contributions" 