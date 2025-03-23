from typing import List
from sqlalchemy.orm import Session
from celery import shared_task
from app.core.celery_app import celery_app
from app.services.sms import sms_service
from app.schemas.sms import SMSType
from app.models.contribution import Contribution
from app.models.member import Member
from app.models.project import Project
from app.core.db import SessionLocal
from app.database import SessionLocal
from app.models.sms import SMS, SMSStatus
from app.services.sms import SMSService

@shared_task
def send_contribution_confirmation(contribution_id: int) -> dict:
    """
    Send SMS confirmation for a contribution.
    """
    db = SessionLocal()
    try:
        contribution = db.query(Contribution).filter(Contribution.id == contribution_id).first()
        if not contribution:
            return {"success": False, "error": "Contribution not found"}

        member = contribution.member
        project = contribution.project

        message = sms_service.format_contribution_message(
            member_name=member.name,
            amount=contribution.amount,
            project_name=project.name
        )

        result = sms_service.send_single_sms(
            phone_number=member.phone_number,
            message=message,
            sms_type=SMSType.CONTRIBUTION
        )

        return {
            "success": result,
            "contribution_id": contribution_id,
            "member_id": member.id
        }
    finally:
        db.close()

@shared_task
def send_pledge_reminders() -> dict:
    """
    Send reminders for pending pledges.
    """
    db = SessionLocal()
    try:
        # Get all pledges without contribution dates
        pending_pledges = db.query(Contribution).filter(
            Contribution.contribution_date.is_(None)
        ).all()

        results = []
        for pledge in pending_pledges:
            message = sms_service.format_pledge_reminder(
                member_name=pledge.member.name,
                amount=pledge.amount,
                project_name=pledge.project.name
            )

            result = sms_service.send_single_sms(
                phone_number=pledge.member.phone_number,
                message=message,
                sms_type=SMSType.PLEDGE_REMINDER
            )

            results.append({
                "success": result,
                "contribution_id": pledge.id,
                "member_id": pledge.member_id
            })

        return {
            "success": all(r["success"] for r in results),
            "total_reminders": len(results),
            "results": results
        }
    finally:
        db.close()

@shared_task
def send_bulk_announcement(message: str, member_ids: List[int] = None) -> dict:
    """
    Send bulk announcement to specified members or all members.
    """
    db = SessionLocal()
    try:
        query = db.query(Member)
        if member_ids:
            query = query.filter(Member.id.in_(member_ids))
        
        members = query.all()
        phone_numbers = [member.phone_number for member in members]
        
        formatted_message = sms_service.format_announcement(message)
        result = sms_service.send_bulk_sms(
            phone_numbers=phone_numbers,
            message=formatted_message,
            sms_type=SMSType.ANNOUNCEMENT
        )

        return {
            "success": result["success"],
            "total_recipients": len(phone_numbers),
            "success_count": result["success_count"],
            "failed_count": result["failed_count"],
            "failed_numbers": result["failed_numbers"]
        }
    finally:
        db.close()

@shared_task
def send_sms(phone_number: str, message: str) -> dict:
    """Send a single SMS."""
    db = SessionLocal()
    try:
        sms_service = SMSService(db)
        sms = sms_service.send_sms(phone_number, message)
        return {"success": True, "sms_id": sms.id}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def send_bulk_sms(phone_numbers: List[str], message: str) -> dict:
    """Send SMS to multiple numbers."""
    db = SessionLocal()
    try:
        sms_service = SMSService(db)
        sms_list = sms_service.send_bulk_sms(phone_numbers, message)
        return {
            "success": True,
            "sent_count": len(sms_list),
            "sms_ids": [sms.id for sms in sms_list]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def update_sms_status(sms_id: int, status: str, error_message: str = None) -> dict:
    """Update SMS status."""
    db = SessionLocal()
    try:
        sms_service = SMSService(db)
        sms = sms_service.update_sms_status(sms_id, SMSStatus(status), error_message)
        return {"success": True, "sms_id": sms.id, "status": sms.status}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close() 