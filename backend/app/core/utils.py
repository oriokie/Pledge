import re
from datetime import datetime
from typing import Optional
import os
import uuid
from decimal import Decimal
import string
import random

def format_phone_number(phone: str) -> str:
    """Format phone number to E.164 format."""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Add country code if number is 10 digits
    if len(digits) == 10:
        digits = "1" + digits
        
    return f"+{digits}"

def validate_phone_number(phone: str) -> bool:
    """Validate phone number format."""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    return len(digits) >= 10 and len(digits) <= 15

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_date_range(start_date: datetime, end_date: datetime) -> bool:
    """Validate date range."""
    return start_date <= end_date

def format_currency(amount: Decimal) -> str:
    """Format amount as currency string."""
    return f"${amount:,.2f}"

def format_date(date: datetime, format: str = "%Y-%m-%d") -> str:
    """Format date string."""
    return date.strftime(format)

def format_percentage(value: float) -> str:
    """Format value as percentage."""
    return f"{value:.2f}%"

def validate_amount(amount: Decimal) -> bool:
    """Validate that amount is positive and not too large."""
    return amount > 0 and amount <= Decimal('1000000000')  # Max 1 billion

def generate_code(prefix: str = "", length: int = 8) -> str:
    """Generate a random code."""
    import random
    import string
    chars = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(chars) for _ in range(length))
    return f"{prefix}{code}" if prefix else code

def sanitize_filename(filename: str) -> str:
    """Sanitize filename."""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename

def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename using timestamp and UUID."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    extension = original_filename.split('.')[-1]
    
    return f"{timestamp}_{unique_id}.{extension}"

def generate_unique_code(prefix: str = "", length: int = 8) -> str:
    """Generate a unique code with optional prefix."""
    unique_id = str(uuid.uuid4())[:length]
    return f"{prefix}{unique_id}" if prefix else unique_id

def generate_random_string(length: int = 8, include_digits: bool = True, include_special: bool = False) -> str:
    """Generate a random string of specified length."""
    chars = string.ascii_letters
    if include_digits:
        chars += string.digits
    if include_special:
        chars += string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def generate_file_name(original_filename: str, prefix: str = "", suffix: str = "") -> str:
    """Generate a unique filename with optional prefix and suffix."""
    name, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    
    # Construct the new filename
    parts = []
    if prefix:
        parts.append(prefix)
    parts.extend([timestamp, unique_id])
    if suffix:
        parts.append(suffix)
    
    return f"{'_'.join(parts)}{ext}" 