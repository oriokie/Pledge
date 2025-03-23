import pytest
from fastapi import status
from app.schemas.sms import SMSRequest, SMSResponse

def test_send_sms(client, admin_token_headers, test_member):
    sms_data = {
        "phone_number": test_member["phone_number"],
        "message": "Test SMS message"
    }
    response = client.post("/api/v1/sms/send", headers=admin_token_headers, json=sms_data)
    assert response.status_code == status.HTTP_200_OK
    sms_response = response.json()
    assert "message_id" in sms_response
    assert "status" in sms_response
    assert sms_response["status"] in ["QUEUED", "SENT", "DELIVERED", "FAILED"]

def test_send_sms_unauthorized(client):
    sms_data = {
        "phone_number": "+1234567890",
        "message": "Test SMS message"
    }
    response = client.post("/api/v1/sms/send", json=sms_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_send_sms_invalid_phone(client, admin_token_headers):
    sms_data = {
        "phone_number": "invalid_phone",
        "message": "Test SMS message"
    }
    response = client.post("/api/v1/sms/send", headers=admin_token_headers, json=sms_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_send_sms_empty_message(client, admin_token_headers, test_member):
    sms_data = {
        "phone_number": test_member["phone_number"],
        "message": ""
    }
    response = client.post("/api/v1/sms/send", headers=admin_token_headers, json=sms_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_send_bulk_sms(client, admin_token_headers, test_member, test_group):
    sms_data = {
        "group_id": test_group["id"],
        "message": "Test bulk SMS message"
    }
    response = client.post("/api/v1/sms/send-bulk", headers=admin_token_headers, json=sms_data)
    assert response.status_code == status.HTTP_200_OK
    bulk_response = response.json()
    assert "total_recipients" in bulk_response
    assert "successful_sends" in bulk_response
    assert "failed_sends" in bulk_response
    assert bulk_response["total_recipients"] >= 1

def test_send_bulk_sms_nonexistent_group(client, admin_token_headers):
    sms_data = {
        "group_id": 999,
        "message": "Test bulk SMS message"
    }
    response = client.post("/api/v1/sms/send-bulk", headers=admin_token_headers, json=sms_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_send_bulk_sms_empty_group(client, admin_token_headers, test_group):
    # Remove all members from the group
    test_group["members"] = []
    
    sms_data = {
        "group_id": test_group["id"],
        "message": "Test bulk SMS message"
    }
    response = client.post("/api/v1/sms/send-bulk", headers=admin_token_headers, json=sms_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Group has no members"

def test_get_sms_status(client, admin_token_headers, test_sms):
    response = client.get(f"/api/v1/sms/status/{test_sms['message_id']}", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    status_response = response.json()
    assert "message_id" in status_response
    assert "status" in status_response
    assert status_response["status"] in ["QUEUED", "SENT", "DELIVERED", "FAILED"]
    assert "sent_at" in status_response
    assert "delivered_at" in status_response

def test_get_sms_status_nonexistent(client, admin_token_headers):
    response = client.get("/api/v1/sms/status/nonexistent_id", headers=admin_token_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_sms_history(client, admin_token_headers, test_sms):
    response = client.get("/api/v1/sms/history", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    history = response.json()
    assert len(history) >= 1
    assert any(sms["message_id"] == test_sms["message_id"] for sms in history)

def test_get_sms_history_with_filters(client, admin_token_headers, test_sms):
    # Test with date range filter
    response = client.get(
        "/api/v1/sms/history",
        headers=admin_token_headers,
        params={
            "start_date": "2024-01-01",
            "end_date": "2024-12-31"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    history = response.json()
    assert len(history) >= 1

    # Test with status filter
    response = client.get(
        "/api/v1/sms/history",
        headers=admin_token_headers,
        params={"status": "SENT"}
    )
    assert response.status_code == status.HTTP_200_OK
    history = response.json()
    assert len(history) >= 1

def test_get_sms_stats(client, admin_token_headers, test_sms):
    response = client.get("/api/v1/sms/stats", headers=admin_token_headers)
    assert response.status_code == status.HTTP_200_OK
    stats = response.json()
    assert "total_sent" in stats
    assert "total_delivered" in stats
    assert "total_failed" in stats
    assert "success_rate" in stats
    assert stats["total_sent"] >= 1
    assert 0 <= stats["success_rate"] <= 100 