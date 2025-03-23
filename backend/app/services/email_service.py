from typing import List, Dict, Any, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from ..core.config import settings

class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Send a single email."""
        try:
            msg = MIMEMultipart()
            msg["From"] = self.smtp_user
            msg["To"] = to_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "html"))

            if attachments:
                for attachment in attachments:
                    part = MIMEApplication(attachment["content"])
                    part.add_header(
                        "Content-Disposition",
                        "attachment",
                        filename=attachment["filename"]
                    )
                    msg.attach(part)

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            return {"status": "success", "message": "Email sent successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def send_bulk_emails(
        self,
        recipients: List[Dict[str, str]],
        subject: str,
        template: str,
        data: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Send bulk emails using a template."""
        results = []
        for recipient in recipients:
            body = template.format(**recipient)
            if data:
                body = body.format(**data)
            result = self.send_email(recipient["email"], subject, body)
            results.append(result)
        return results 