from .models import *

# This will ensure all models are registered with SQLAlchemy's metadata
__all__ = [
    "Base",
    "User",
    "UserRole",
    "Member",
    "Group",
    "group_member",
    "Project",
    "Contribution",
    "SMS",
    "SMSStatus",
    "Notification",
    "File",
    "Pledge",
    "PledgeStatus"
]

# Let SQLAlchemy handle table creation order
Base.metadata.create_all = lambda *args, **kwargs: None 