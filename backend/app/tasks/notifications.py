from celery import shared_task
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.notification_service import NotificationService

@shared_task
def send_contribution_notification(contribution_id: int) -> dict:
    """Send notification for a new contribution."""
    db = SessionLocal()
    try:
        notification_service = NotificationService(db)
        notification = notification_service.send_contribution_notification(contribution_id)
        return {"success": True, "notification_id": notification.id}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def send_project_update_notification(project_id: int, message: str) -> dict:
    """Send notification for project updates."""
    db = SessionLocal()
    try:
        notification_service = NotificationService(db)
        notifications = notification_service.send_project_update_notification(project_id, message)
        return {
            "success": True,
            "notification_count": len(notifications),
            "notification_ids": [n.id for n in notifications]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def send_reminder_notification(member_id: int, message: str) -> dict:
    """Send reminder notification to a member."""
    db = SessionLocal()
    try:
        notification_service = NotificationService(db)
        notification = notification_service.send_reminder_notification(member_id, message)
        return {"success": True, "notification_id": notification.id}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def send_bulk_notification(group_id: int, message: str) -> dict:
    """Send notification to all members in a group."""
    db = SessionLocal()
    try:
        notification_service = NotificationService(db)
        notifications = notification_service.send_bulk_notification(group_id, message)
        return {
            "success": True,
            "notification_count": len(notifications),
            "notification_ids": [n.id for n in notifications]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def mark_notification_as_read(notification_id: int) -> dict:
    """Mark a notification as read."""
    db = SessionLocal()
    try:
        notification_service = NotificationService(db)
        notification = notification_service.mark_as_read(notification_id)
        return {"success": True, "notification_id": notification.id}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def delete_old_notifications(days: int = 30) -> dict:
    """Delete notifications older than specified days."""
    db = SessionLocal()
    try:
        notification_service = NotificationService(db)
        count = notification_service.delete_old_notifications(days)
        return {"success": True, "deleted_count": count}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close() 