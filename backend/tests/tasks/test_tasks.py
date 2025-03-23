import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from app.tasks.sms import send_sms, send_bulk_sms, update_sms_status
from app.tasks.reports import generate_contribution_report, generate_member_report, generate_project_report, generate_group_report, generate_daily_report, generate_weekly_report, generate_monthly_report
from app.tasks.notifications import send_contribution_notification, send_project_update_notification, send_reminder_notification
from app.tasks.cleanup import cleanup_old_sms
from app.models.sms import SMS
from app.models.contribution import Contribution
from app.models.project import Project
from app.models.member import Member
import time

@pytest.fixture
def mock_celery():
    """Mock Celery app"""
    with patch("app.tasks.sms.celery_app") as mock:
        yield mock

@pytest.fixture
def mock_sms_service():
    """Mock SMS service"""
    with patch("app.services.sms_service") as mock:
        mock.send_sms.return_value = {"status": "success", "message_id": "123"}
        yield mock

@pytest.fixture
def mock_report_service():
    """Mock report service"""
    with patch("app.services.report_service") as mock:
        mock.generate_report.return_value = "report_data"
        yield mock

def test_send_sms_task(test_member):
    result = send_sms.delay(
        phone_number=test_member["phone_number"],
        message="Test SMS message"
    )
    assert result.get(timeout=10)["status"] in ["QUEUED", "SENT", "DELIVERED", "FAILED"]
    assert "message_id" in result.get(timeout=10)

def test_send_bulk_sms_task(test_group):
    result = send_bulk_sms.delay(
        group_id=test_group["id"],
        message="Test bulk SMS message"
    )
    response = result.get(timeout=10)
    assert response["total_recipients"] >= 1
    assert response["successful_sends"] >= 0
    assert response["failed_sends"] >= 0

def test_update_sms_status_task(test_sms):
    result = update_sms_status.delay(test_sms["message_id"])
    status = result.get(timeout=10)
    assert status in ["QUEUED", "SENT", "DELIVERED", "FAILED"]
    assert "sent_at" in result.info
    assert "delivered_at" in result.info

def test_generate_contribution_report_task(test_contribution):
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    result = generate_contribution_report.delay(
        start_date=start_date,
        end_date=end_date
    )
    report = result.get(timeout=10)
    assert "total_amount" in report
    assert "contribution_count" in report
    assert "average_amount" in report
    assert "contributions_by_date" in report
    assert "contributions_by_payment_method" in report
    assert "contributions_by_project" in report

def test_generate_member_report_task(test_member, test_contribution):
    result = generate_member_report.delay(test_member["id"])
    report = result.get(timeout=10)
    assert report["member_id"] == test_member["id"]
    assert report["total_contributions"] >= 1
    assert report["total_amount"] >= test_contribution["amount"]
    assert "contributions_by_project" in report
    assert "contribution_history" in report

def test_generate_project_report_task(test_project, test_contribution):
    result = generate_project_report.delay(test_project["id"])
    report = result.get(timeout=10)
    assert report["project_id"] == test_project["id"]
    assert report["total_contributions"] >= 1
    assert report["total_amount"] >= test_contribution["amount"]
    assert report["progress_percentage"] >= 0
    assert report["progress_percentage"] <= 100
    assert "contributions_by_date" in report
    assert "contributions_by_payment_method" in report
    assert "top_contributors" in report

def test_generate_group_report_task(test_group, test_contribution):
    result = generate_group_report.delay(test_group["id"])
    report = result.get(timeout=10)
    assert report["group_id"] == test_group["id"]
    assert report["member_count"] >= 1
    assert report["total_contributions"] >= 1
    assert report["total_amount"] >= test_contribution["amount"]
    assert "contributions_by_member" in report
    assert "contributions_by_project" in report
    assert "contribution_history" in report

def test_send_contribution_notification_task(test_contribution):
    result = send_contribution_notification.delay(
        contribution_id=test_contribution["id"],
        notification_type="RECEIPT"
    )
    assert result.get(timeout=10)["status"] == "SENT"
    assert "notification_id" in result.get(timeout=10)

def test_send_project_update_notification_task(test_project):
    result = send_project_update_notification.delay(
        project_id=test_project["id"],
        update_type="PROGRESS"
    )
    assert result.get(timeout=10)["status"] == "SENT"
    assert "notification_id" in result.get(timeout=10)

def test_send_reminder_notification_task(test_member, test_project):
    result = send_reminder_notification.delay(
        member_id=test_member["id"],
        project_id=test_project["id"],
        reminder_type="PAYMENT"
    )
    assert result.get(timeout=10)["status"] == "SENT"
    assert "notification_id" in result.get(timeout=10)

def test_task_retry_on_failure():
    # Test retry mechanism for failed tasks
    result = send_sms.delay(
        phone_number="invalid_phone",
        message="Test message"
    )
    with pytest.raises(Exception):
        result.get(timeout=10)
    assert result.retries > 0

def test_task_celery_chain():
    # Test chaining multiple tasks
    from celery import chain
    
    task_chain = chain(
        generate_contribution_report.s(),
        send_contribution_notification.s()
    )
    
    result = task_chain.delay()
    final_result = result.get(timeout=10)
    assert final_result["status"] == "SENT"
    assert "notification_id" in final_result

def test_task_celery_group():
    # Test parallel execution of tasks
    from celery import group
    
    tasks = group(
        send_sms.s("+1234567890", "Message 1"),
        send_sms.s("+0987654321", "Message 2")
    )
    
    results = tasks.delay()
    assert len(results.get(timeout=10)) == 2
    assert all(r["status"] in ["QUEUED", "SENT", "DELIVERED", "FAILED"] for r in results.get(timeout=10))

def test_send_sms_success(mock_celery, mock_sms_service):
    """Test successful SMS sending"""
    # Test data
    phone_number = "+254712345678"
    message = "Test message"
    
    # Send SMS
    result = send_sms.delay(phone_number, message)
    
    # Verify task was called
    assert result.get() == {"status": "success", "message_id": "123"}
    mock_sms_service.send_sms.assert_called_once_with(phone_number, message)

def test_send_sms_failure(mock_celery, mock_sms_service):
    """Test failed SMS sending"""
    # Configure mock to raise exception
    mock_sms_service.send_sms.side_effect = Exception("SMS service error")
    
    # Test data
    phone_number = "+254712345678"
    message = "Test message"
    
    # Send SMS
    result = send_sms.delay(phone_number, message)
    
    # Verify task failed
    with pytest.raises(Exception):
        result.get()

def test_generate_daily_report(mock_celery, mock_report_service):
    """Test daily report generation"""
    # Test data
    date = datetime.now().date()
    
    # Generate report
    result = generate_daily_report.delay(date)
    
    # Verify report was generated
    assert result.get() == "report_data"
    mock_report_service.generate_report.assert_called_once_with(
        "daily",
        start_date=date,
        end_date=date
    )

def test_generate_weekly_report(mock_celery, mock_report_service):
    """Test weekly report generation"""
    # Test data
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=6)
    
    # Generate report
    result = generate_weekly_report.delay(start_date, end_date)
    
    # Verify report was generated
    assert result.get() == "report_data"
    mock_report_service.generate_report.assert_called_once_with(
        "weekly",
        start_date=start_date,
        end_date=end_date
    )

def test_generate_monthly_report(mock_celery, mock_report_service):
    """Test monthly report generation"""
    # Test data
    year = 2024
    month = 1
    
    # Generate report
    result = generate_monthly_report.delay(year, month)
    
    # Verify report was generated
    assert result.get() == "report_data"
    mock_report_service.generate_report.assert_called_once_with(
        "monthly",
        year=year,
        month=month
    )

def test_generate_project_report(mock_celery, mock_report_service):
    """Test project report generation"""
    # Test data
    project_id = 1
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=30)
    
    # Generate report
    result = generate_project_report.delay(project_id, start_date, end_date)
    
    # Verify report was generated
    assert result.get() == "report_data"
    mock_report_service.generate_report.assert_called_once_with(
        "project",
        project_id=project_id,
        start_date=start_date,
        end_date=end_date
    )

def test_cleanup_old_sms(mock_celery):
    """Test cleanup of old SMS records"""
    # Mock database session
    mock_db = MagicMock()
    
    # Test data
    old_date = datetime.now() - timedelta(days=30)
    mock_db.query.return_value.filter.return_value.all.return_value = [
        SMS(id=1, created_at=old_date),
        SMS(id=2, created_at=old_date)
    ]
    
    # Cleanup old SMS
    result = cleanup_old_sms.delay()
    
    # Verify cleanup was performed
    assert result.get() == {"deleted_count": 2}
    mock_db.query.return_value.filter.return_value.delete.assert_called_once()
    mock_db.commit.assert_called_once()

def test_task_retry(mock_celery, mock_sms_service):
    """Test task retry mechanism"""
    # Configure mock to fail first time, succeed second time
    mock_sms_service.send_sms.side_effect = [
        Exception("First attempt failed"),
        {"status": "success", "message_id": "123"}
    ]
    
    # Test data
    phone_number = "+254712345678"
    message = "Test message"
    
    # Send SMS with retry
    result = send_sms.delay(phone_number, message)
    
    # Verify task succeeded after retry
    assert result.get() == {"status": "success", "message_id": "123"}
    assert mock_sms_service.send_sms.call_count == 2

def test_task_timeout(mock_celery, mock_sms_service):
    """Test task timeout"""
    # Configure mock to delay longer than timeout
    mock_sms_service.send_sms.side_effect = lambda *args, **kwargs: time.sleep(2)
    
    # Test data
    phone_number = "+254712345678"
    message = "Test message"
    
    # Send SMS with timeout
    result = send_sms.delay(phone_number, message)
    
    # Verify task timed out
    with pytest.raises(Exception):
        result.get(timeout=1) 