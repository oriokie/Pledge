# Core Components

## Security

The system implements several security measures to protect data and ensure secure operations:

### Authentication
```python
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token
)

# Password hashing
hashed_password = get_password_hash("user_password")
is_valid = verify_password("user_password", hashed_password)

# JWT tokens
token = create_access_token({"sub": "user@example.com"})
payload = verify_token(token)
```

Key features:
- Bcrypt password hashing
- JWT token-based authentication
- Token expiration and refresh
- Secure password reset flow

### Database

The system uses SQLAlchemy ORM with PostgreSQL:

```python
from app.core.db import SessionLocal, engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

# Use database session
with SessionLocal() as db:
    # Perform database operations
    db.add(user)
    db.commit()
```

Features:
- Connection pooling
- Transaction management
- Migration support with Alembic
- Automatic schema generation

### Dependencies

FastAPI dependency injection system:

```python
from app.core.deps import (
    get_db,
    get_current_user,
    get_current_active_user,
    get_current_admin_user
)

@app.get("/users/me")
def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user
```

Key dependencies:
- Database session
- Current user
- Role-based access
- Authentication verification

### Utilities

Common utility functions:

```python
from app.core.utils import (
    validate_phone_number,
    validate_email,
    validate_date_range,
    format_currency,
    format_date
)

# Validation
is_valid = validate_phone_number("+254712345678")
is_valid = validate_email("user@example.com")

# Formatting
amount = format_currency(1000, "USD")
date = format_date(datetime.now(), "%Y-%m-%d")
```

Available utilities:
- Phone number validation
- Email validation
- Date range validation
- Currency formatting
- Date formatting
- Percentage formatting
- Code generation
- File name handling

## Configuration

Environment variables (`.env`):
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/db_name

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Storage
STORAGE_BACKEND=s3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_BUCKET_NAME=your-bucket

# SMS
SMS_PROVIDER=africastalking
SMS_API_KEY=your-api-key
SMS_SENDER_ID=your-sender-id

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Error Handling

Custom exception classes:

```python
from app.core.exceptions import (
    StorageError,
    SMSError,
    EmailError,
    NotificationError,
    ReportError
)

try:
    # Operation that might fail
    raise StorageError("Failed to upload file")
except StorageError as e:
    # Handle storage error
    logger.error(f"Storage error: {str(e)}")
```

Error types:
- StorageError: File storage operations
- SMSError: SMS sending operations
- EmailError: Email sending operations
- NotificationError: Notification operations
- ReportError: Report generation operations

## Logging

Logging configuration:

```python
import logging
from app.core.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Log messages
logger.info("Operation successful")
logger.error("Operation failed", exc_info=True)
```

Features:
- Multiple handlers (file, console)
- Log rotation
- Different log levels
- Exception tracking
- Request logging 