from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.sms import SMS, SMSStatus
from app.core.exceptions import SMSError

class SMSService:
    def __init__(self, db: Session):
        self.db = db

    def send_sms(self, phone_number: str, message: str) -> SMS:
        """Send a single SMS."""
        try:
            # Create SMS record
            sms = SMS(
                phone_number=phone_number,
                message=message,
                status=SMSStatus.PENDING
            )
            self.db.add(sms)
            self.db.commit()
            self.db.refresh(sms)

            # TODO: Integrate with actual SMS provider
            # For now, just mark as sent
            sms.status = SMSStatus.SENT
            self.db.commit()
            self.db.refresh(sms)

            return sms
        except Exception as e:
            self.db.rollback()
            raise SMSError(f"Failed to send SMS: {str(e)}")

    def send_bulk_sms(self, phone_numbers: List[str], message: str) -> List[SMS]:
        """Send SMS to multiple numbers."""
        sms_list = []
        for phone_number in phone_numbers:
            try:
                sms = self.send_sms(phone_number, message)
                sms_list.append(sms)
            except SMSError as e:
                # Log error but continue with other numbers
                continue
        return sms_list

    def update_sms_status(self, sms_id: int, status: SMSStatus, error_message: Optional[str] = None) -> SMS:
        """Update SMS status."""
        sms = self.db.query(SMS).filter(SMS.id == sms_id).first()
        if not sms:
            raise SMSError(f"SMS with id {sms_id} not found")
        
        sms.status = status
        if error_message:
            sms.error_message = error_message
        
        self.db.commit()
        self.db.refresh(sms)
        return sms

sms_service = SMSService(None)  # Will be initialized with db session when needed 