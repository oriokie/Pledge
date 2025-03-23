from celery import shared_task
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.report_service import ReportService

@shared_task
def generate_contribution_report(start_date: str, end_date: str) -> dict:
    """Generate contribution report."""
    db = SessionLocal()
    try:
        report_service = ReportService(db)
        report = report_service.generate_contribution_report(start_date, end_date)
        return {"success": True, "report": report}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def generate_member_report(member_id: int) -> dict:
    """Generate member report."""
    db = SessionLocal()
    try:
        report_service = ReportService(db)
        report = report_service.generate_member_report(member_id)
        return {"success": True, "report": report}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def generate_project_report(project_id: int) -> dict:
    """Generate project report."""
    db = SessionLocal()
    try:
        report_service = ReportService(db)
        report = report_service.generate_project_report(project_id)
        return {"success": True, "report": report}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def generate_group_report(group_id: int) -> dict:
    """Generate group report."""
    db = SessionLocal()
    try:
        report_service = ReportService(db)
        report = report_service.generate_group_report(group_id)
        return {"success": True, "report": report}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def generate_daily_report() -> dict:
    """Generate daily report."""
    db = SessionLocal()
    try:
        report_service = ReportService(db)
        report = report_service.generate_daily_report()
        return {"success": True, "report": report}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def generate_weekly_report() -> dict:
    """Generate weekly report."""
    db = SessionLocal()
    try:
        report_service = ReportService(db)
        report = report_service.generate_weekly_report()
        return {"success": True, "report": report}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close()

@shared_task
def generate_monthly_report() -> dict:
    """Generate monthly report."""
    db = SessionLocal()
    try:
        report_service = ReportService(db)
        report = report_service.generate_monthly_report()
        return {"success": True, "report": report}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        db.close() 