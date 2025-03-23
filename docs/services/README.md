# Services

## Storage Service

The storage service handles file operations with support for multiple backends:

```python
from app.services.storage_service import StorageService

storage = StorageService()

# Upload file
result = storage.upload_file("test.pdf", file_content, backend="s3")
file_url = result["url"]

# Download file
result = storage.download_file(file_url)
content = result["content"]

# Delete file
result = storage.delete_file(file_url)
```

Features:
- Multiple storage backends (local, S3)
- File upload/download
- File deletion
- URL generation
- Backend validation
- Error handling

## Email Service

The email service handles email sending operations:

```python
from app.services.email_service import EmailService

email = EmailService()

# Send single email
result = email.send_email(
    to_email="user@example.com",
    subject="Test Subject",
    body="Test Body",
    attachments=[
        {
            "filename": "test.pdf",
            "content": pdf_content,
            "content_type": "application/pdf"
        }
    ]
)

# Send bulk emails
results = email.send_bulk_emails(
    recipients=[
        {"email": "user1@example.com", "name": "User One"},
        {"email": "user2@example.com", "name": "User Two"}
    ],
    subject="Test Subject",
    template="Hello {name}, this is a test email."
)
```

Features:
- SMTP support
- HTML email support
- File attachments
- Email templates
- Bulk sending
- Error handling

## SMS Service

The SMS service handles SMS sending operations:

```python
from app.services.sms_service import SMSService

sms = SMSService()

# Send single SMS
result = sms.send_sms(
    phone_number="+254712345678",
    message="Test message"
)

# Send bulk SMS
results = sms.send_bulk_sms([
    {"phone": "+254712345678", "message": "Message 1"},
    {"phone": "+254712345679", "message": "Message 2"}
])

# Check status
status = sms.get_sms_status(message_id)
```

Features:
- Multiple providers support
- Bulk SMS sending
- Status tracking
- Message templates
- Phone validation
- Error handling

## File Service

The file service handles file operations:

```python
from app.services.file_service import FileService

file_service = FileService()

# Upload file
result = file_service.upload_file(file_name, file_content)

# Download file
result = file_service.download_file(file_url)

# Delete file
result = file_service.delete_file(file_url)

# Validate file
is_valid = file_service.validate_file_type("test.pdf", ["pdf", "doc"])
is_valid = file_service.validate_file_size(file_size, max_size=10*1024*1024)
```

Features:
- File upload/download
- File validation
- File type checking
- Size validation
- Name generation
- Error handling

## Notification Service

The notification service handles user notifications:

```python
from app.services.notification_service import NotificationService

notification = NotificationService()

# Send contribution notification
result = notification.send_contribution_notification(
    contribution=contribution,
    member=member
)

# Send project update
result = notification.send_project_update_notification(
    project=project,
    users=users
)

# Send reminder
result = notification.send_reminder_notification(
    member=member,
    project=project
)

# Send bulk notifications
result = notification.send_bulk_notifications(
    users=users,
    template=template,
    data=data
)
```

Features:
- Multiple channels (email, SMS)
- Templates support
- Bulk notifications
- User preferences
- Error handling

## Report Service

The report service handles report generation:

```python
from app.services.report_service import ReportService

report = ReportService()

# Generate daily report
result = report.generate_daily_report(date)

# Generate project report
result = report.generate_project_report(
    project_id=1,
    start_date=start_date,
    end_date=end_date
)

# Export report
file_path = report.export_report_to_excel(report_data, "report_name")
file_path = report.export_report_to_pdf(report_data, "report_name")
```

Features:
- Multiple report types
- Date range filtering
- Multiple export formats
- Data aggregation
- Error handling

## Background Tasks

Celery tasks for asynchronous operations:

```python
from app.tasks.sms import send_sms
from app.tasks.reports import generate_daily_report
from app.tasks.notifications import send_contribution_notification

# Send SMS asynchronously
result = send_sms.delay(phone_number, message)

# Generate report asynchronously
result = generate_daily_report.delay(date)

# Send notification asynchronously
result = send_contribution_notification.delay(contribution_id)
```

Features:
- Task queues
- Task scheduling
- Task retries
- Task chaining
- Error handling 