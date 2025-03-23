from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.notification import Notification
from ..models.member import Member
from ..core.utils import format_date

class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    def create_notification(
        self,
        member_id: int,
        title: str,
        message: str,
        notification_type: str,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a new notification."""
        try:
            notification = Notification(
                member_id=member_id,
                title=title,
                message=message,
                type=notification_type,
                data=data,
                is_read=False
            )
            self.db.add(notification)
            self.db.commit()

            return {
                "status": "success",
                "notification_id": notification.id,
                "message": "Notification created successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_member_notifications(
        self,
        member_id: int,
        is_read: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Get notifications for a member."""
        try:
            query = self.db.query(Notification).filter(Notification.member_id == member_id)

            if is_read is not None:
                query = query.filter(Notification.is_read == is_read)

            total_count = query.count()
            notifications = query.order_by(Notification.created_at.desc()).offset(offset).limit(limit).all()

            return {
                "status": "success",
                "total_count": total_count,
                "notifications": [
                    {
                        "id": n.id,
                        "title": n.title,
                        "message": n.message,
                        "type": n.type,
                        "data": n.data,
                        "is_read": n.is_read,
                        "created_at": format_date(n.created_at)
                    }
                    for n in notifications
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def mark_notification_read(
        self,
        notification_id: int,
        member_id: int
    ) -> Dict[str, Any]:
        """Mark a notification as read."""
        try:
            notification = self.db.query(Notification).filter(
                Notification.id == notification_id,
                Notification.member_id == member_id
            ).first()

            if not notification:
                return {"status": "error", "message": "Notification not found"}

            notification.is_read = True
            notification.read_at = datetime.utcnow()
            self.db.commit()

            return {
                "status": "success",
                "message": "Notification marked as read"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def mark_all_notifications_read(
        self,
        member_id: int
    ) -> Dict[str, Any]:
        """Mark all notifications as read for a member."""
        try:
            self.db.query(Notification).filter(
                Notification.member_id == member_id,
                Notification.is_read == False
            ).update({
                "is_read": True,
                "read_at": datetime.utcnow()
            })
            self.db.commit()

            return {
                "status": "success",
                "message": "All notifications marked as read"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_notification(
        self,
        notification_id: int,
        member_id: int
    ) -> Dict[str, Any]:
        """Delete a notification."""
        try:
            notification = self.db.query(Notification).filter(
                Notification.id == notification_id,
                Notification.member_id == member_id
            ).first()

            if not notification:
                return {"status": "error", "message": "Notification not found"}

            self.db.delete(notification)
            self.db.commit()

            return {
                "status": "success",
                "message": "Notification deleted successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_unread_count(
        self,
        member_id: int
    ) -> Dict[str, Any]:
        """Get count of unread notifications."""
        try:
            count = self.db.query(Notification).filter(
                Notification.member_id == member_id,
                Notification.is_read == False
            ).count()

            return {
                "status": "success",
                "unread_count": count
            }
        except Exception as e:
            return {"status": "error", "message": str(e)} 