class AppError(Exception):
    """Base exception for all application errors."""
    pass

class EmailError(AppError):
    """Exception raised for email-related errors."""
    pass

class FileError(AppError):
    """Exception raised for file-related errors."""
    pass

class StorageError(AppError):
    """Exception raised for storage-related errors."""
    pass

class NotificationError(AppError):
    """Exception raised for notification-related errors."""
    pass

class ReportError(AppError):
    """Exception raised for report-related errors."""
    pass

class SMSError(AppError):
    """Exception raised for SMS-related errors."""
    pass

class ValidationError(AppError):
    """Exception raised for validation errors."""
    pass

class AuthenticationError(AppError):
    """Exception raised for authentication errors."""
    pass

class AuthorizationError(AppError):
    """Exception raised for authorization errors."""
    pass

class DatabaseError(AppError):
    """Exception raised for database-related errors."""
    pass 