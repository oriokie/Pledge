import pytest
from fastapi import status
from datetime import datetime, timedelta

def test_get_contribution_report(client, admin_token_headers, test_contribution):
    # Test with date range
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    response = client.get(
        "/api/v1/reports/contributions",
        headers=admin_token_headers,
        params={
            "start_date": start_date,
            "end_date": end_date
        }
    )
    assert response.status_code == status.HTTP_200_OK
    report = response.json()
    assert "total_amount" in report
    assert "contribution_count" in report
    assert "average_amount" in report
    assert "contributions_by_date" in report
    assert "contributions_by_payment_method" in report
    assert "contributions_by_project" in report

def test_get_contribution_report_with_filters(client, admin_token_headers, test_contribution):
    # Test with project filter
    response = client.get(
        "/api/v1/reports/contributions",
        headers=admin_token_headers,
        params={"project_id": test_contribution["project"]["id"]}
    )
    assert response.status_code == status.HTTP_200_OK
    report = response.json()
    assert report["total_amount"] >= test_contribution["amount"]

    # Test with payment method filter
    response = client.get(
        "/api/v1/reports/contributions",
        headers=admin_token_headers,
        params={"payment_method": test_contribution["payment_method"]}
    )
    assert response.status_code == status.HTTP_200_OK
    report = response.json()
    assert report["total_amount"] >= test_contribution["amount"]

def test_get_member_report(client, admin_token_headers, test_member, test_contribution):
    response = client.get(
        f"/api/v1/reports/members/{test_member['id']}",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    report = response.json()
    assert report["member_id"] == test_member["id"]
    assert report["total_contributions"] >= 1
    assert report["total_amount"] >= test_contribution["amount"]
    assert "contributions_by_project" in report
    assert "contribution_history" in report

def test_get_member_report_nonexistent(client, admin_token_headers):
    response = client.get(
        "/api/v1/reports/members/999",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_project_report(client, admin_token_headers, test_project, test_contribution):
    response = client.get(
        f"/api/v1/reports/projects/{test_project['id']}",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    report = response.json()
    assert report["project_id"] == test_project["id"]
    assert report["total_contributions"] >= 1
    assert report["total_amount"] >= test_contribution["amount"]
    assert report["progress_percentage"] >= 0
    assert report["progress_percentage"] <= 100
    assert "contributions_by_date" in report
    assert "contributions_by_payment_method" in report
    assert "top_contributors" in report

def test_get_project_report_nonexistent(client, admin_token_headers):
    response = client.get(
        "/api/v1/reports/projects/999",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_group_report(client, admin_token_headers, test_group, test_contribution):
    response = client.get(
        f"/api/v1/reports/groups/{test_group['id']}",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    report = response.json()
    assert report["group_id"] == test_group["id"]
    assert report["member_count"] >= 1
    assert report["total_contributions"] >= 1
    assert report["total_amount"] >= test_contribution["amount"]
    assert "contributions_by_member" in report
    assert "contributions_by_project" in report
    assert "contribution_history" in report

def test_get_group_report_nonexistent(client, admin_token_headers):
    response = client.get(
        "/api/v1/reports/groups/999",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_summary_report(client, admin_token_headers, test_contribution):
    response = client.get(
        "/api/v1/reports/summary",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    report = response.json()
    assert "total_contributions" in report
    assert "total_amount" in report
    assert "average_amount" in report
    assert "total_members" in report
    assert "total_projects" in report
    assert "total_groups" in report
    assert "contributions_by_month" in report
    assert "top_contributors" in report
    assert "top_projects" in report
    assert "top_groups" in report

def test_get_summary_report_with_date_range(client, admin_token_headers, test_contribution):
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    response = client.get(
        "/api/v1/reports/summary",
        headers=admin_token_headers,
        params={
            "start_date": start_date,
            "end_date": end_date
        }
    )
    assert response.status_code == status.HTTP_200_OK
    report = response.json()
    assert report["total_amount"] >= test_contribution["amount"]

def test_export_contribution_report(client, admin_token_headers, test_contribution):
    response = client.get(
        "/api/v1/reports/contributions/export",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert response.headers["content-disposition"].startswith("attachment; filename=contributions_report_")

def test_export_member_report(client, admin_token_headers, test_member):
    response = client.get(
        f"/api/v1/reports/members/{test_member['id']}/export",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert response.headers["content-disposition"].startswith("attachment; filename=member_report_")

def test_export_project_report(client, admin_token_headers, test_project):
    response = client.get(
        f"/api/v1/reports/projects/{test_project['id']}/export",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert response.headers["content-disposition"].startswith("attachment; filename=project_report_")

def test_export_group_report(client, admin_token_headers, test_group):
    response = client.get(
        f"/api/v1/reports/groups/{test_group['id']}/export",
        headers=admin_token_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert response.headers["content-disposition"].startswith("attachment; filename=group_report_") 