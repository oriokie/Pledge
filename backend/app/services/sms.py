import requests
from app.core.config import settings
from typing import List, Optional

class SMSService:
    def __init__(self):
        self.api_key = settings.ADVANTA_SMS_API_KEY
        self.sender_id = settings.ADVANTA_SMS_SENDER_ID
        self.base_url = "https://api.advantasms.com/v1"  # Replace with actual Advanta SMS API URL
    
    def send_single_sms(self, phone_number: str, message: str) -> bool:
        """Send a single SMS to a phone number"""
        try:
            response = requests.post(
                f"{self.base_url}/messages",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "sender_id": self.sender_id,
                    "phone_number": phone_number,
                    "message": message
                }
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending SMS: {str(e)}")
            return False
    
    def send_bulk_sms(self, phone_numbers: List[str], message: str) -> bool:
        """Send SMS to multiple phone numbers"""
        try:
            response = requests.post(
                f"{self.base_url}/messages/bulk",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "sender_id": self.sender_id,
                    "phone_numbers": phone_numbers,
                    "message": message
                }
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending bulk SMS: {str(e)}")
            return False
    
    def send_pledge_confirmation(self, phone_number: str, amount: float, project_name: str) -> bool:
        """Send pledge confirmation SMS"""
        message = f"Thank you for pledging {amount} to {project_name}. We will send you reminders for your contribution."
        return self.send_single_sms(phone_number, message)
    
    def send_contribution_confirmation(self, phone_number: str, amount: float, project_name: str) -> bool:
        """Send contribution confirmation SMS"""
        message = f"Thank you for your contribution of {amount} to {project_name}. Your contribution has been recorded."
        return self.send_single_sms(phone_number, message)
    
    def send_pledge_reminder(self, phone_number: str, amount: float, project_name: str) -> bool:
        """Send pledge reminder SMS"""
        message = f"Reminder: You have pledged {amount} to {project_name}. Please make your contribution when possible."
        return self.send_single_sms(phone_number, message)

sms_service = SMSService() 