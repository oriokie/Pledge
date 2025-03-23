import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.services.email_service import EmailService
from app.core.exceptions import EmailError

@pytest.fixture
def email_service():
    """Create email service instance"""
    return EmailService()

@pytest.fixture
def mock_smtp():
    """Mock SMTP server"""
    with patch("app.services.email_service.smtplib.SMTP") as mock:
        mock_instance = MagicMock()
        mock_instance.sendmail.return_value = {}
        mock.return_value.__enter__.return_value = mock_instance
        yield mock

def test_send_email_success(email_service, mock_smtp):
    """Test successful email sending"""
    # Test data
    to_email = "test@example.com"
    subject = "Test Subject"
    body = "Test Body"
    
    # Send email
    result = email_service.send_email(to_email, subject, body)
    
    # Verify result
    assert result["status"] == "success"
    assert "message_id" in result
    
    # Verify SMTP was called
    mock_smtp.return_value.__enter__.return_value.sendmail.assert_called_once()

def test_send_email_with_attachments(email_service, mock_smtp):
    """Test email sending with attachments"""
    # Test data
    to_email = "test@example.com"
    subject = "Test Subject"
    body = "Test Body"
    attachments = [
        {"filename": "test.pdf", "content": b"test content", "content_type": "application/pdf"}
    ]
    
    # Send email
    result = email_service.send_email(to_email, subject, body, attachments=attachments)
    
    # Verify result
    assert result["status"] == "success"
    assert "message_id" in result
    
    # Verify SMTP was called with attachments
    mock_smtp.return_value.__enter__.return_value.sendmail.assert_called_once()

def test_send_email_failure(email_service, mock_smtp):
    """Test failed email sending"""
    # Configure mock to raise exception
    mock_smtp.return_value.__enter__.return_value.sendmail.side_effect = Exception("SMTP error")
    
    # Test data
    to_email = "test@example.com"
    subject = "Test Subject"
    body = "Test Body"
    
    # Send email
    with pytest.raises(EmailError) as exc_info:
        email_service.send_email(to_email, subject, body)
    
    # Verify error
    assert str(exc_info.value) == "Failed to send email: SMTP error"

def test_send_bulk_emails(email_service, mock_smtp):
    """Test bulk email sending"""
    # Test data
    recipients = [
        {"email": "user1@example.com", "name": "User One"},
        {"email": "user2@example.com", "name": "User Two"}
    ]
    subject = "Test Subject"
    template = "Hello {name}, this is a test email."
    
    # Send emails
    results = email_service.send_bulk_emails(recipients, subject, template)
    
    # Verify results
    assert len(results) == 2
    assert all(r["status"] == "success" for r in results)
    
    # Verify SMTP was called for each recipient
    assert mock_smtp.return_value.__enter__.return_value.sendmail.call_count == 2

def test_render_email_template(email_service):
    """Test email template rendering"""
    # Test data
    template = "Hello {name}, your contribution of {amount} has been received."
    data = {
        "name": "John",
        "amount": "1000"
    }
    
    # Render template
    body = email_service.render_template(template, data)
    
    # Verify body
    assert body == "Hello John, your contribution of 1000 has been received."
    
    # Test with missing data
    with pytest.raises(KeyError):
        email_service.render_template(template, {"name": "John"})

def test_email_validation(email_service):
    """Test email validation"""
    # Valid emails
    assert email_service.validate_email("test@example.com") is True
    assert email_service.validate_email("user.name@domain.co.uk") is True
    assert email_service.validate_email("test+label@example.com") is True
    
    # Invalid emails
    assert email_service.validate_email("invalid") is False
    assert email_service.validate_email("test@") is False
    assert email_service.validate_email("@domain.com") is False

def test_email_encoding(email_service):
    """Test email encoding"""
    # Test data
    subject = "Test Subject with Unicode: 你好"
    body = "Test Body with Unicode: 你好"
    
    # Encode email
    encoded_subject, encoded_body = email_service.encode_email(subject, body)
    
    # Verify encoding
    assert isinstance(encoded_subject, str)
    assert isinstance(encoded_body, str)
    assert "你好" in encoded_subject
    assert "你好" in encoded_body

def test_email_headers(email_service):
    """Test email headers"""
    # Test data
    to_email = "test@example.com"
    subject = "Test Subject"
    
    # Generate headers
    headers = email_service.generate_headers(to_email, subject)
    
    # Verify headers
    assert "From" in headers
    assert "To" in headers
    assert "Subject" in headers
    assert "Date" in headers
    assert "Message-ID" in headers

def test_email_cleanup(email_service):
    """Test email cleanup"""
    # Test data
    email = "  test@example.com  "
    
    # Clean email
    cleaned_email = email_service.clean_email(email)
    
    # Verify cleanup
    assert cleaned_email == "test@example.com" 