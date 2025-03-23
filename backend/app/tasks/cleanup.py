from celery import shared_task
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.sms import SMS, SMSStatus
from app.models.notification import Notification
from app.models.file import File

@shared_task
def cleanup_old_sms(days: int = 30) -> dict:
    """Delete SMS records older than specified days."""
    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        deleted_count = db.query(SMS).filter(
            SMS.created_at < cutoff_date,
            SMS.status.in_([SMSStatus.SENT, SMSStatus.FAILED, SMSStatus.DELIVERED])
        ).delete(synchronize_session=False)
        db.commit()
        return {"success": True, "deleted_count": deleted_count}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def cleanup_old_notifications(days: int = 30) -> dict:
    """Delete notifications older than specified days."""
    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        deleted_count = db.query(Notification).filter(
            Notification.created_at < cutoff_date,
            Notification.is_read == True
        ).delete(synchronize_session=False)
        db.commit()
        return {"success": True, "deleted_count": deleted_count}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def cleanup_old_files(days: int = 30) -> dict:
    """Delete files older than specified days."""
    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        old_files = db.query(File).filter(
            File.created_at < cutoff_date,
            File.is_deleted == False
        ).all()
        
        deleted_count = 0
        for file in old_files:
            try:
                # TODO: Delete actual file from storage
                file.is_deleted = True
                deleted_count += 1
            except Exception:
                continue
        
        db.commit()
        return {"success": True, "deleted_count": deleted_count}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def cleanup_all() -> dict:
    """Run all cleanup tasks."""
    sms_result = cleanup_old_sms.delay()
    notifications_result = cleanup_old_notifications.delay()
    files_result = cleanup_old_files.delay()
    
    return {
        "sms_task_id": sms_result.id,
        "notifications_task_id": notifications_result.id,
        "files_task_id": files_result.id
    } 