from typing import Dict, Any, List, Optional
import requests
from datetime import datetime
from ..core.utils import validate_phone_number
from ..core.config import settings
from ..models.sms import SMS
from sqlalchemy.orm import Session

class SMSService:
    def __init__(self):
        self.api_key = settings.SMS_API_KEY
        self.api_url = settings.SMS_API_URL
        self.sender_id = settings.SMS_SENDER_ID

    def validate_phone_number(self, phone_number: str) -> bool:
        """Validate phone number format."""
        return validate_phone_number(phone_number)

    def send_sms(
        self,
        phone_number: str,
        message: str,
        db: Session,
        member_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Send a single SMS."""
        try:
            if not self.validate_phone_number(phone_number):
                return {"status": "error", "message": "Invalid phone number format"}

            # Create SMS record
            sms = SMS(
                phone_number=phone_number,
                message=message,
                status="pending",
                member_id=member_id
            )
            db.add(sms)
            db.commit()

            # Send SMS via API
            payload = {
                "api_key": self.api_key,
                "phone_number": phone_number,
                "message": message,
                "sender_id": self.sender_id
            }

            response = requests.post(self.api_url, json=payload)
            response_data = response.json()

            # Update SMS record
            if response_data.get("status") == "success":
                sms.status = "sent"
                sms.sent_at = datetime.utcnow()
            else:
                sms.status = "failed"
                sms.error_message = response_data.get("message", "Unknown error")

            db.commit()

            return {
                "status": sms.status,
                "message": "SMS sent successfully" if sms.status == "sent" else sms.error_message,
                "sms_id": sms.id
            }

        except Exception as e:
            if "sms" in locals():
                sms.status = "failed"
                sms.error_message = str(e)
                db.commit()
            return {"status": "error", "message": str(e)}

    def send_bulk_sms(
        self,
        recipients: List[Dict[str, str]],
        message_template: str,
        db: Session
    ) -> List[Dict[str, Any]]:
        """Send bulk SMS messages."""
        results = []
        for recipient in recipients:
            message = message_template.format(**recipient)
            result = self.send_sms(
                phone_number=recipient["phone_number"],
                message=message,
                db=db,
                member_id=recipient.get("member_id")
            )
            results.append(result)
        return results

    def get_sms_status(self, sms_id: int, db: Session) -> Dict[str, Any]:
        """Get SMS status."""
        try:
            sms = db.query(SMS).filter(SMS.id == sms_id).first()
            if not sms:
                return {"status": "error", "message": "SMS not found"}

            return {
                "status": "success",
                "sms_id": sms.id,
                "phone_number": sms.phone_number,
                "message": sms.message,
                "status": sms.status,
                "error_message": sms.error_message,
                "created_at": sms.created_at,
                "sent_at": sms.sent_at
            }
        except Exception as e:
            return {"status": "error", "message": str(e)} 