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

# Ensure tables are created in the correct order
tables_order = [
    User.__table__,
    Member.__table__,
    Group.__table__,
    group_member,
    Project.__table__,
    Contribution.__table__,
    SMS.__table__,
    Notification.__table__,
    File.__table__
]

# Update metadata to reflect the correct order
for table in tables_order:
    if table.name not in Base.metadata.tables:
        Base.metadata._add_table(table.name, table.schema, table) 