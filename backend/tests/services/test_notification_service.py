import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.services.notification_service import NotificationService
from app.models.user import User
from app.models.member import Member
from app.models.contribution import Contribution
from app.models.project import Project
from app.core.exceptions import NotificationError

@pytest.fixture
def notification_service():
    """Create notification service instance"""
    return NotificationService()

@pytest.fixture
def mock_email_service():
    """Mock email service"""
    with patch("app.services.notification_service.EmailService") as mock:
        mock_instance = MagicMock()
        mock_instance.send_email.return_value = {"status": "success", "message_id": "123"}
        mock.return_value = mock_instance
        yield mock

@pytest.fixture
def mock_sms_service():
    """Mock SMS service"""
    with patch("app.services.notification_service.SMSService") as mock:
        mock_instance = MagicMock()
        mock_instance.send_sms.return_value = {"status": "success", "message_id": "123"}
        mock.return_value = mock_instance
        yield mock

def test_send_contribution_notification(notification_service, mock_email_service, mock_sms_service):
    """Test contribution notification"""
    # Test data
    contribution = Contribution(
        id=1,
        amount=1000,
        created_at=datetime.now()
    )
    member = Member(
        id=1,
        name="John Doe",
        phone_number="+254712345678",
        email="john@example.com"
    )
    
    # Send notification
    result = notification_service.send_contribution_notification(contribution, member)
    
    # Verify result
    assert result["status"] == "success"
    assert "email_sent" in result
    assert "sms_sent" in result
    
    # Verify services were called
    mock_email_service.return_value.send_email.assert_called_once()
    mock_sms_service.return_value.send_sms.assert_called_once()

def test_send_project_update_notification(notification_service, mock_email_service):
    """Test project update notification"""
    # Test data
    project = Project(
        id=1,
        name="Test Project",
        description="Test Description"
    )
    users = [
        User(
            id=1,
            email="user1@example.com",
            full_name="User One"
        ),
        User(
            id=2,
            email="user2@example.com",
            full_name="User Two"
        )
    ]
    
    # Send notification
    result = notification_service.send_project_update_notification(project, users)
    
    # Verify result
    assert result["status"] == "success"
    assert result["notifications_sent"] == 2
    
    # Verify service was called for each user
    assert mock_email_service.return_value.send_email.call_count == 2

def test_send_reminder_notification(notification_service, mock_email_service, mock_sms_service):
    """Test reminder notification"""
    # Test data
    member = Member(
        id=1,
        name="John Doe",
        phone_number="+254712345678",
        email="john@example.com"
    )
    project = Project(
        id=1,
        name="Test Project",
        target_amount=10000
    )
    
    # Send notification
    result = notification_service.send_reminder_notification(member, project)
    
    # Verify result
    assert result["status"] == "success"
    assert "email_sent" in result
    assert "sms_sent" in result
    
    # Verify services were called
    mock_email_service.return_value.send_email.assert_called_once()
    mock_sms_service.return_value.send_sms.assert_called_once()

def test_send_bulk_notifications(notification_service, mock_email_service):
    """Test bulk notifications"""
    # Test data
    users = [
        User(
            id=1,
            email="user1@example.com",
            full_name="User One"
        ),
        User(
            id=2,
            email="user2@example.com",
            full_name="User Two"
        )
    ]
    template = "test_template"
    data = {"key": "value"}
    
    # Send notifications
    result = notification_service.send_bulk_notifications(users, template, data)
    
    # Verify result
    assert result["status"] == "success"
    assert result["notifications_sent"] == 2
    
    # Verify service was called for each user
    assert mock_email_service.return_value.send_email.call_count == 2

def test_notification_error_handling(notification_service, mock_email_service):
    """Test notification error handling"""
    # Configure mock to raise exception
    mock_email_service.return_value.send_email.side_effect = Exception("Email service error")
    
    # Test data
    user = User(
        id=1,
        email="user@example.com",
        full_name="Test User"
    )
    template = "test_template"
    data = {"key": "value"}
    
    # Send notification
    with pytest.raises(NotificationError) as exc_info:
        notification_service.send_notification(user, template, data)
    
    # Verify error
    assert str(exc_info.value) == "Failed to send notification: Email service error"

def test_notification_template_rendering(notification_service):
    """Test notification template rendering"""
    # Test data
    template = "Hello {name}, your contribution of {amount} has been received."
    data = {
        "name": "John",
        "amount": "1000"
    }
    
    # Render template
    message = notification_service.render_template(template, data)
    
    # Verify message
    assert message == "Hello John, your contribution of 1000 has been received."
    
    # Test with missing data
    with pytest.raises(KeyError):
        notification_service.render_template(template, {"name": "John"})

def test_notification_preferences(notification_service, mock_email_service, mock_sms_service):
    """Test notification preferences"""
    # Test data
    user = User(
        id=1,
        email="user@example.com",
        full_name="Test User",
        notification_preferences={
            "email": True,
            "sms": False
        }
    )
    template = "test_template"
    data = {"key": "value"}
    
    # Send notification
    result = notification_service.send_notification(user, template, data)
    
    # Verify result
    assert result["status"] == "success"
    assert result["email_sent"] is True
    assert result["sms_sent"] is False
    
    # Verify only email service was called
    mock_email_service.return_value.send_email.assert_called_once()
    mock_sms_service.return_value.send_sms.assert_not_called() 