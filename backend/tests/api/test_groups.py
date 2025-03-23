import pytest
from fastapi import status
from app.schemas.group import GroupCreate, GroupUpdate

def test_read_groups(client, admin_token_headers, test_group):
    response = client.get("/api/v1/groups/", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    groups = response.json()
    assert len(groups) >= 1
    assert any(group["name"] == test_group["name"] for group in groups)

def test_read_groups_unauthorized(client):
    response = client.get("/api/v1/groups/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_group(client, admin_token_headers, test_member):
    group_data = {
        "name": "New Group",
        "member_ids": [test_member["id"]]
    }
    response = client.post("/api/v1/groups/", headers=admin_token_headers, json=group_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_group = response.json()
    assert created_group["name"] == group_data["name"]
    assert len(created_group["members"]) == 1
    assert created_group["members"][0]["id"] == test_member["id"]

def test_create_group_duplicate_name(client, admin_token_headers, test_group):
    group_data = {
        "name": test_group["name"],
        "member_ids": []
    }
    response = client.post("/api/v1/groups/", headers=admin_token_headers, json=group_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_group_nonexistent_member(client, admin_token_headers):
    group_data = {
        "name": "New Group",
        "member_ids": [999]
    }
    response = client.post("/api/v1/groups/", headers=admin_token_headers, json=group_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_read_group(client, admin_token_headers, test_group):
    response = client.get(f"/api/v1/groups/{test_group['id']}", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    group = response.json()
    assert group["name"] == test_group["name"]
    assert "members" in group

def test_read_group_nonexistent(client, admin_token_headers):
    response = client.get("/api/v1/groups/999", headers=admin_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_group(client, admin_token_headers, test_group, test_member):
    update_data = {
        "name": "Updated Group",
        "member_ids": [test_member["id"]]
    }
    response = client.put(
        f"/api/v1/groups/{test_group['id']}",
        headers=admin_token_headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    updated_group = response.json()
    assert updated_group["name"] == update_data["name"]
    assert len(updated_group["members"]) == 1
    assert updated_group["members"][0]["id"] == test_member["id"]

def test_update_group_duplicate_name(client, admin_token_headers, test_group, db):
    # Create another group
    other_group = Group(name="Other Group")
    db.add(other_group)
    db.commit()
    
    update_data = {
        "name": other_group.name
    }
    response = client.put(
        f"/api/v1/groups/{test_group['id']}",
        headers=admin_token_headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_update_group_nonexistent(client, admin_token_headers):
    update_data = {
        "name": "Updated Group",
        "member_ids": []
    }
    response = client.put(
        "/api/v1/groups/999",
        headers=admin_token_headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_group_nonexistent_member(client, admin_token_headers, test_group):
    update_data = {
        "member_ids": [999]
    }
    response = client.put(
        f"/api/v1/groups/{test_group['id']}",
        headers=admin_token_headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_group(client, admin_token_headers, test_group):
    response = client.delete(f"/api/v1/groups/{test_group['id']}", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    deleted_group = response.json()
    assert deleted_group["name"] == test_group["name"]

def test_delete_group_nonexistent(client, admin_token_headers):
    response = client.delete("/api/v1/groups/999", headers=admin_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_group_with_contributions(client, admin_token_headers, test_group, test_contribution):
    response = client.delete(f"/api/v1/groups/{test_group['id']}", headers=admin_token_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Cannot delete group with existing contributions"

def test_get_group_stats(client, admin_token_headers, test_group, test_contribution):
    response = client.get(f"/api/v1/groups/{test_group['id']}/stats", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    stats = response.json()
    assert stats["member_count"] >= 1
    assert stats["contribution_count"] >= 1
    assert stats["total_amount"] >= 0
    assert stats["group_name"] == test_group["name"] 