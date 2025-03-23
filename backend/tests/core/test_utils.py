import pytest
from datetime import datetime, timedelta
from app.core.utils import (
    validate_phone_number,
    validate_email,
    validate_date_range,
    validate_amount,
    format_currency,
    format_date,
    format_phone_number,
    format_percentage,
    generate_unique_code,
    generate_random_string,
    generate_file_name
)

def test_validate_phone_number():
    """Test phone number validation"""
    # Valid phone numbers
    assert validate_phone_number("+254712345678") is True
    assert validate_phone_number("254712345678") is True
    assert validate_phone_number("0712345678") is True
    
    # Invalid phone numbers
    assert validate_phone_number("123") is False
    assert validate_phone_number("abc") is False
    assert validate_phone_number("+254123") is False

def test_validate_email():
    """Test email validation"""
    # Valid emails
    assert validate_email("test@example.com") is True
    assert validate_email("user.name@domain.co.uk") is True
    assert validate_email("test+label@example.com") is True
    
    # Invalid emails
    assert validate_email("invalid") is False
    assert validate_email("test@") is False
    assert validate_email("@domain.com") is False

def test_validate_date_range():
    """Test date range validation"""
    # Valid date range
    start_date = datetime.now()
    end_date = start_date + timedelta(days=7)
    assert validate_date_range(start_date, end_date) is True
    
    # Invalid date range (end before start)
    assert validate_date_range(end_date, start_date) is False
    
    # Invalid date range (same date)
    assert validate_date_range(start_date, start_date) is False

def test_validate_amount():
    """Test amount validation"""
    # Valid amounts
    assert validate_amount(100) is True
    assert validate_amount(100.50) is True
    assert validate_amount(0) is True
    
    # Invalid amounts
    assert validate_amount(-100) is False
    assert validate_amount("100") is False
    assert validate_amount(None) is False

def test_format_currency():
    """Test currency formatting"""
    # Test with different amounts
    assert format_currency(1000) == "1,000.00"
    assert format_currency(1000.5) == "1,000.50"
    assert format_currency(0) == "0.00"
    
    # Test with different currencies
    assert format_currency(1000, currency="USD") == "1,000.00 USD"
    assert format_currency(1000, currency="EUR") == "1,000.00 EUR"

def test_format_date():
    """Test date formatting"""
    date = datetime(2024, 1, 1, 12, 0)
    
    # Test different formats
    assert format_date(date) == "2024-01-01"
    assert format_date(date, format="%d/%m/%Y") == "01/01/2024"
    assert format_date(date, format="%Y-%m-%d %H:%M") == "2024-01-01 12:00"

def test_format_phone_number():
    """Test phone number formatting"""
    # Test different formats
    assert format_phone_number("+254712345678") == "+254 712 345 678"
    assert format_phone_number("254712345678") == "+254 712 345 678"
    assert format_phone_number("0712345678") == "+254 712 345 678"

def test_format_percentage():
    """Test percentage formatting"""
    # Test with different values
    assert format_percentage(50) == "50.00%"
    assert format_percentage(50.5) == "50.50%"
    assert format_percentage(0) == "0.00%"
    
    # Test with different decimal places
    assert format_percentage(50.555, decimals=1) == "50.6%"
    assert format_percentage(50.555, decimals=2) == "50.56%"

def test_generate_unique_code():
    """Test unique code generation"""
    # Test code format
    code = generate_unique_code()
    assert len(code) == 8
    assert code.isalnum()
    assert code.isupper()
    
    # Test uniqueness
    codes = [generate_unique_code() for _ in range(100)]
    assert len(set(codes)) == 100

def test_generate_random_string():
    """Test random string generation"""
    # Test with different lengths
    assert len(generate_random_string(10)) == 10
    assert len(generate_random_string(20)) == 20
    
    # Test with different character types
    string = generate_random_string(10, include_digits=True, include_special=True)
    assert any(c.isdigit() for c in string)
    assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in string)

def test_generate_file_name():
    """Test file name generation"""
    # Test with different extensions
    assert generate_file_name("test", "pdf").endswith(".pdf")
    assert generate_file_name("test", "docx").endswith(".docx")
    
    # Test with different prefixes
    assert generate_file_name("test", "pdf", prefix="user_").startswith("user_")
    
    # Test uniqueness
    names = [generate_file_name("test", "pdf") for _ in range(100)]
    assert len(set(names)) == 100 