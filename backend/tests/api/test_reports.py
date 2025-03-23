from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

def test_get_project_report(client: TestClient, test_user_token_headers: dict) -> None:
    # First create a project
    project_data = {
        "name": "Test Project",
        "description": "Test Project Description",
        "target_amount": 10000.0,
        "start_date": datetime.now(),
        "end_date": datetime.now() + timedelta(days=30),
        "status": "active",
    }
    project_response = client.post("/api/v1/projects/", headers=test_user_token_headers, json=project_data)
    project_id = project_response.json()["id"]
    
    # Create a member
    member_data = {
        "name": "Test Member",
        "phone_number": "1234567891",
        "alias": "TM",
        "is_active": True,
    }
    member_response = client.post("/api/v1/members/", headers=test_user_token_headers, json=member_data)
    member_id = member_response.json()["id"]
    
    # Create a contribution
    contribution_data = {
        "member_id": member_id,
        "project_id": project_id,
        "amount": 1000.0,
        "type": "contribution",
    }
    client.post("/api/v1/contributions/", headers=test_user_token_headers, json=contribution_data)
    
    # Get project report
    response = client.get(f"/api/v1/reports/projects/{project_id}", headers=test_user_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) > 0
    assert "Date" in content[0]
    assert "Member Code" in content[0]
    assert "Member Name" in content[0]
    assert "Amount" in content[0]

def test_get_project_report_not_found(client: TestClient, test_user_token_headers: dict) -> None:
    response = client.get("/api/v1/reports/projects/999", headers=test_user_token_headers)
    assert response.status_code == 404
    assert "detail" in response.json()

def test_get_group_report(client: TestClient, test_user_token_headers: dict) -> None:
    # First create a group
    group_data = {
        "name": "Test Group",
        "description": "Test Group Description",
    }
    group_response = client.post("/api/v1/groups/", headers=test_user_token_headers, json=group_data)
    group_id = group_response.json()["id"]
    
    # Create a member
    member_data = {
        "name": "Test Member",
        "phone_number": "1234567892",
        "alias": "TM",
        "is_active": True,
    }
    member_response = client.post("/api/v1/members/", headers=test_user_token_headers, json=member_data)
    member_id = member_response.json()["id"]
    
    # Add member to group
    client.post(f"/api/v1/groups/{group_id}/members/{member_id}", headers=test_user_token_headers)
    
    # Create a project
    project_data = {
        "name": "Test Project",
        "description": "Test Project Description",
        "target_amount": 10000.0,
        "start_date": datetime.now(),
        "end_date": datetime.now() + timedelta(days=30),
        "status": "active",
    }
    project_response = client.post("/api/v1/projects/", headers=test_user_token_headers, json=project_data)
    project_id = project_response.json()["id"]
    
    # Create a contribution
    contribution_data = {
        "member_id": member_id,
        "project_id": project_id,
        "group_id": group_id,
        "amount": 1000.0,
        "type": "contribution",
    }
    client.post("/api/v1/contributions/", headers=test_user_token_headers, json=contribution_data)
    
    # Get group report
    response = client.get(f"/api/v1/reports/groups/{group_id}", headers=test_user_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) > 0
    assert "Date" in content[0]
    assert "Member Code" in content[0]
    assert "Member Name" in content[0]
    assert "Project" in content[0]
    assert "Amount" in content[0]

def test_get_group_report_not_found(client: TestClient, test_user_token_headers: dict) -> None:
    response = client.get("/api/v1/reports/groups/999", headers=test_user_token_headers)
    assert response.status_code == 404
    assert "detail" in response.json()

def test_get_member_report(client: TestClient, test_user_token_headers: dict) -> None:
    # Create a member
    member_data = {
        "name": "Test Member",
        "phone_number": "1234567893",
        "alias": "TM",
        "is_active": True,
    }
    member_response = client.post("/api/v1/members/", headers=test_user_token_headers, json=member_data)
    member_id = member_response.json()["id"]
    
    # Create a project
    project_data = {
        "name": "Test Project",
        "description": "Test Project Description",
        "target_amount": 10000.0,
        "start_date": datetime.now(),
        "end_date": datetime.now() + timedelta(days=30),
        "status": "active",
    }
    project_response = client.post("/api/v1/projects/", headers=test_user_token_headers, json=project_data)
    project_id = project_response.json()["id"]
    
    # Create a contribution
    contribution_data = {
        "member_id": member_id,
        "project_id": project_id,
        "amount": 1000.0,
        "type": "contribution",
    }
    client.post("/api/v1/contributions/", headers=test_user_token_headers, json=contribution_data)
    
    # Get member report
    response = client.get(f"/api/v1/reports/members/{member_id}", headers=test_user_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)
    assert len(content) > 0
    assert "Date" in content[0]
    assert "Project" in content[0]
    assert "Amount" in content[0]

def test_get_member_report_not_found(client: TestClient, test_user_token_headers: dict) -> None:
    response = client.get("/api/v1/reports/members/999", headers=test_user_token_headers)
    assert response.status_code == 404
    assert "detail" in response.json()

def test_get_dashboard_data(client: TestClient, test_user_token_headers: dict) -> None:
    response = client.get("/api/v1/reports/dashboard", headers=test_user_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert "total_pledged" in content
    assert "total_contributed" in content
    assert "remaining_balance" in content
    assert "top_groups" in content
    assert "active_projects" in content

def test_download_project_report(client: TestClient, test_user_token_headers: dict) -> None:
    # First create a project
    project_data = {
        "name": "Test Project",
        "description": "Test Project Description",
        "target_amount": 10000.0,
        "start_date": datetime.now(),
        "end_date": datetime.now() + timedelta(days=30),
        "status": "active",
    }
    project_response = client.post("/api/v1/projects/", headers=test_user_token_headers, json=project_data)
    project_id = project_response.json()["id"]
    
    # Create a member
    member_data = {
        "name": "Test Member",
        "phone_number": "1234567894",
        "alias": "TM",
        "is_active": True,
    }
    member_response = client.post("/api/v1/members/", headers=test_user_token_headers, json=member_data)
    member_id = member_response.json()["id"]
    
    # Create a contribution
    contribution_data = {
        "member_id": member_id,
        "project_id": project_id,
        "amount": 1000.0,
        "type": "contribution",
    }
    client.post("/api/v1/contributions/", headers=test_user_token_headers, json=contribution_data)
    
    # Download project report
    response = client.get(
        f"/api/v1/reports/projects/{project_id}?download=true",
        headers=test_user_token_headers
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert "filename" in response.headers["content-disposition"] 