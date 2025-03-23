import pytest
from fastapi import status
from app.schemas.contribution import ContributionCreate, ContributionUpdate

def test_read_contributions(client, admin_token_headers, test_contribution):
    response = client.get("/api/v1/contributions/", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    contributions = response.json()
    assert len(contributions) >= 1
    assert any(contribution["id"] == test_contribution["id"] for contribution in contributions)

def test_read_contributions_unauthorized(client):
    response = client.get("/api/v1/contributions/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_contribution(client, admin_token_headers, test_member, test_project):
    contribution_data = {
        "member_id": test_member["id"],
        "project_id": test_project["id"],
        "amount": 1000.0,
        "payment_method": "CASH",
        "payment_date": "2024-01-01",
        "notes": "Test contribution"
    }
    response = client.post("/api/v1/contributions/", headers=admin_token_headers, json=contribution_data)
    assert response.status_code == status.HTTP_201_CREATED
    created_contribution = response.json()
    assert created_contribution["amount"] == contribution_data["amount"]
    assert created_contribution["payment_method"] == contribution_data["payment_method"]
    assert created_contribution["payment_date"] == contribution_data["payment_date"]
    assert created_contribution["notes"] == contribution_data["notes"]
    assert created_contribution["member"]["id"] == test_member["id"]
    assert created_contribution["project"]["id"] == test_project["id"]

def test_create_contribution_nonexistent_member(client, admin_token_headers, test_project):
    contribution_data = {
        "member_id": 999,
        "project_id": test_project["id"],
        "amount": 1000.0,
        "payment_method": "CASH",
        "payment_date": "2024-01-01"
    }
    response = client.post("/api/v1/contributions/", headers=admin_token_headers, json=contribution_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_contribution_nonexistent_project(client, admin_token_headers, test_member):
    contribution_data = {
        "member_id": test_member["id"],
        "project_id": 999,
        "amount": 1000.0,
        "payment_method": "CASH",
        "payment_date": "2024-01-01"
    }
    response = client.post("/api/v1/contributions/", headers=admin_token_headers, json=contribution_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_contribution_invalid_amount(client, admin_token_headers, test_member, test_project):
    contribution_data = {
        "member_id": test_member["id"],
        "project_id": test_project["id"],
        "amount": -1000.0,
        "payment_method": "CASH",
        "payment_date": "2024-01-01"
    }
    response = client.post("/api/v1/contributions/", headers=admin_token_headers, json=contribution_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_read_contribution(client, admin_token_headers, test_contribution):
    response = client.get(f"/api/v1/contributions/{test_contribution['id']}", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    contribution = response.json()
    assert contribution["id"] == test_contribution["id"]
    assert contribution["amount"] == test_contribution["amount"]
    assert contribution["payment_method"] == test_contribution["payment_method"]
    assert contribution["payment_date"] == test_contribution["payment_date"]
    assert "member" in contribution
    assert "project" in contribution

def test_read_contribution_nonexistent(client, admin_token_headers):
    response = client.get("/api/v1/contributions/999", headers=admin_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_contribution(client, admin_token_headers, test_contribution):
    update_data = {
        "amount": 2000.0,
        "payment_method": "BANK_TRANSFER",
        "payment_date": "2024-02-01",
        "notes": "Updated contribution"
    }
    response = client.put(
        f"/api/v1/contributions/{test_contribution['id']}",
        headers=admin_token_headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    updated_contribution = response.json()
    assert updated_contribution["amount"] == update_data["amount"]
    assert updated_contribution["payment_method"] == update_data["payment_method"]
    assert updated_contribution["payment_date"] == update_data["payment_date"]
    assert updated_contribution["notes"] == update_data["notes"]

def test_update_contribution_nonexistent(client, admin_token_headers):
    update_data = {
        "amount": 2000.0,
        "payment_method": "BANK_TRANSFER",
        "payment_date": "2024-02-01"
    }
    response = client.put(
        "/api/v1/contributions/999",
        headers=admin_token_headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_contribution_invalid_amount(client, admin_token_headers, test_contribution):
    update_data = {
        "amount": -2000.0
    }
    response = client.put(
        f"/api/v1/contributions/{test_contribution['id']}",
        headers=admin_token_headers,
        json=update_data
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_delete_contribution(client, admin_token_headers, test_contribution):
    response = client.delete(f"/api/v1/contributions/{test_contribution['id']}", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    deleted_contribution = response.json()
    assert deleted_contribution["id"] == test_contribution["id"]

def test_delete_contribution_nonexistent(client, admin_token_headers):
    response = client.delete("/api/v1/contributions/999", headers=admin_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_member_contributions(client, admin_token_headers, test_member, test_contribution):
    response = client.get(f"/api/v1/contributions/member/{test_member['id']}", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    contributions = response.json()
    assert len(contributions) >= 1
    assert any(contribution["id"] == test_contribution["id"] for contribution in contributions)

def test_get_project_contributions(client, admin_token_headers, test_project, test_contribution):
    response = client.get(f"/api/v1/contributions/project/{test_project['id']}", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    contributions = response.json()
    assert len(contributions) >= 1
    assert any(contribution["id"] == test_contribution["id"] for contribution in contributions)

def test_get_contribution_stats(client, admin_token_headers, test_contribution):
    response = client.get("/api/v1/contributions/stats", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    stats = response.json()
    assert "total_amount" in stats
    assert "contribution_count" in stats
    assert "average_amount" in stats
    assert stats["contribution_count"] >= 1
    assert stats["total_amount"] >= 0
    assert stats["average_amount"] >= 0 