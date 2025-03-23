from .base import Base
from .user import User, UserRole
from .member import Member
from .group import Group, group_member
from .project import Project
from .contribution import Contribution
from .sms import SMS, SMSStatus
from .notification import Notification
from .file import File

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
    "File"
]

# Let SQLAlchemy handle table creation order
Base.metadata.create_all = lambda *args, **kwargs: None 