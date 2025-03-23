import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.services.sms_service import SMSService
from app.models.sms import SMS, SMSStatus
from app.core.exceptions import SMSError

@pytest.fixture
def sms_service():
    """Create SMS service instance"""
    return SMSService()

@pytest.fixture
def mock_sms_provider():
    """Mock SMS provider"""
    with patch("app.services.sms_service.SMSProvider") as mock:
        mock_instance = MagicMock()
        mock_instance.send_sms.return_value = {"status": "success", "message_id": "123"}
        mock.return_value = mock_instance
        yield mock

def test_send_sms_success(sms_service, mock_sms_provider):
    """Test successful SMS sending"""
    # Test data
    phone_number = "+254712345678"
    message = "Test message"
    
    # Send SMS
    result = sms_service.send_sms(phone_number, message)
    
    # Verify result
    assert result["status"] == "success"
    assert result["message_id"] == "123"
    
    # Verify provider was called
    mock_sms_provider.return_value.send_sms.assert_called_once_with(
        phone_number,
        message
    )

def test_send_sms_failure(sms_service, mock_sms_provider):
    """Test failed SMS sending"""
    # Configure mock to raise exception
    mock_sms_provider.return_value.send_sms.side_effect = Exception("Provider error")
    
    # Test data
    phone_number = "+254712345678"
    message = "Test message"
    
    # Send SMS
    with pytest.raises(SMSError) as exc_info:
        sms_service.send_sms(phone_number, message)
    
    # Verify error
    assert str(exc_info.value) == "Failed to send SMS: Provider error"

def test_send_bulk_sms(sms_service, mock_sms_provider):
    """Test bulk SMS sending"""
    # Test data
    messages = [
        {"phone": "+254712345678", "message": "Message 1"},
        {"phone": "+254712345679", "message": "Message 2"}
    ]
    
    # Send bulk SMS
    results = sms_service.send_bulk_sms(messages)
    
    # Verify results
    assert len(results) == 2
    assert all(r["status"] == "success" for r in results)
    
    # Verify provider was called for each message
    assert mock_sms_provider.return_value.send_sms.call_count == 2

def test_update_sms_status(sms_service, mock_sms_provider):
    """Test SMS status update"""
    # Test data
    message_id = "123"
    status = "DELIVERED"
    
    # Update status
    result = sms_service.update_sms_status(message_id, status)
    
    # Verify result
    assert result["status"] == "success"
    assert result["message_id"] == message_id
    
    # Verify provider was called
    mock_sms_provider.return_value.check_status.assert_called_once_with(message_id)

def test_get_sms_status(sms_service, mock_sms_provider):
    """Test getting SMS status"""
    # Test data
    message_id = "123"
    mock_sms_provider.return_value.check_status.return_value = "DELIVERED"
    
    # Get status
    status = sms_service.get_sms_status(message_id)
    
    # Verify status
    assert status == "DELIVERED"
    
    # Verify provider was called
    mock_sms_provider.return_value.check_status.assert_called_once_with(message_id)

def test_get_sms_history(sms_service, mock_sms_provider):
    """Test getting SMS history"""
    # Test data
    phone_number = "+254712345678"
    mock_sms_provider.return_value.get_history.return_value = [
        {"message_id": "123", "status": "DELIVERED"},
        {"message_id": "124", "status": "SENT"}
    ]
    
    # Get history
    history = sms_service.get_sms_history(phone_number)
    
    # Verify history
    assert len(history) == 2
    assert all("message_id" in h for h in history)
    assert all("status" in h for h in history)
    
    # Verify provider was called
    mock_sms_provider.return_value.get_history.assert_called_once_with(phone_number)

def test_get_sms_balance(sms_service, mock_sms_provider):
    """Test getting SMS balance"""
    # Test data
    mock_sms_provider.return_value.get_balance.return_value = 100
    
    # Get balance
    balance = sms_service.get_sms_balance()
    
    # Verify balance
    assert balance == 100
    
    # Verify provider was called
    mock_sms_provider.return_value.get_balance.assert_called_once()

def test_validate_phone_number(sms_service):
    """Test phone number validation"""
    # Valid phone numbers
    assert sms_service.validate_phone_number("+254712345678") is True
    assert sms_service.validate_phone_number("254712345678") is True
    assert sms_service.validate_phone_number("0712345678") is True
    
    # Invalid phone numbers
    assert sms_service.validate_phone_number("123") is False
    assert sms_service.validate_phone_number("abc") is False
    assert sms_service.validate_phone_number("+254123") is False

def test_format_message(sms_service):
    """Test message formatting"""
    # Test data
    template = "Hello {name}, your contribution of {amount} has been received."
    data = {"name": "John", "amount": "1000"}
    
    # Format message
    message = sms_service.format_message(template, data)
    
    # Verify message
    assert message == "Hello John, your contribution of 1000 has been received."
    
    # Test with missing data
    with pytest.raises(KeyError):
        sms_service.format_message(template, {"name": "John"}) 