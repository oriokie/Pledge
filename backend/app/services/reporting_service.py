from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from ..models.contribution import Contribution
from ..models.member import Member
from ..models.group import Group
from ..core.utils import format_currency, format_date, format_percentage

class ReportingService:
    def __init__(self, db: Session):
        self.db = db

    def get_contribution_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        group_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get contribution summary for a period."""
        try:
            query = self.db.query(Contribution)

            if start_date:
                query = query.filter(Contribution.created_at >= start_date)
            if end_date:
                query = query.filter(Contribution.created_at <= end_date)
            if group_id:
                query = query.filter(Contribution.group_id == group_id)

            total_amount = query.with_entities(func.sum(Contribution.amount)).scalar() or 0
            total_count = query.count()
            avg_amount = total_amount / total_count if total_count > 0 else 0

            return {
                "status": "success",
                "total_amount": format_currency(total_amount),
                "total_count": total_count,
                "average_amount": format_currency(avg_amount),
                "period": {
                    "start_date": format_date(start_date) if start_date else None,
                    "end_date": format_date(end_date) if end_date else None
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_member_contribution_report(
        self,
        member_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get detailed contribution report for a member."""
        try:
            query = self.db.query(Contribution).filter(Contribution.member_id == member_id)

            if start_date:
                query = query.filter(Contribution.created_at >= start_date)
            if end_date:
                query = query.filter(Contribution.created_at <= end_date)

            contributions = query.order_by(Contribution.created_at.desc()).all()
            total_amount = sum(c.amount for c in contributions)

            return {
                "status": "success",
                "member_id": member_id,
                "total_contributions": len(contributions),
                "total_amount": format_currency(total_amount),
                "contributions": [
                    {
                        "id": c.id,
                        "amount": format_currency(c.amount),
                        "date": format_date(c.created_at),
                        "group": c.group.name if c.group else None,
                        "status": c.status
                    }
                    for c in contributions
                ],
                "period": {
                    "start_date": format_date(start_date) if start_date else None,
                    "end_date": format_date(end_date) if end_date else None
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_group_performance_report(
        self,
        group_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get performance report for a group."""
        try:
            group = self.db.query(Group).filter(Group.id == group_id).first()
            if not group:
                return {"status": "error", "message": "Group not found"}

            query = self.db.query(Contribution).filter(Contribution.group_id == group_id)

            if start_date:
                query = query.filter(Contribution.created_at >= start_date)
            if end_date:
                query = query.filter(Contribution.created_at <= end_date)

            contributions = query.all()
            total_amount = sum(c.amount for c in contributions)
            member_count = len(group.members)
            avg_contribution = total_amount / member_count if member_count > 0 else 0

            return {
                "status": "success",
                "group_id": group_id,
                "group_name": group.name,
                "total_contributions": len(contributions),
                "total_amount": format_currency(total_amount),
                "member_count": member_count,
                "average_contribution": format_currency(avg_contribution),
                "period": {
                    "start_date": format_date(start_date) if start_date else None,
                    "end_date": format_date(end_date) if end_date else None
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_trend_analysis(
        self,
        group_id: Optional[int] = None,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get contribution trends over time."""
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)

            query = self.db.query(
                func.date(Contribution.created_at).label("date"),
                func.sum(Contribution.amount).label("total_amount"),
                func.count(Contribution.id).label("contribution_count")
            ).filter(
                and_(
                    Contribution.created_at >= start_date,
                    Contribution.created_at <= end_date
                )
            )

            if group_id:
                query = query.filter(Contribution.group_id == group_id)

            results = query.group_by("date").order_by("date").all()

            return {
                "status": "success",
                "trends": [
                    {
                        "date": format_date(r.date),
                        "total_amount": format_currency(r.total_amount),
                        "contribution_count": r.contribution_count
                    }
                    for r in results
                ],
                "period": {
                    "start_date": format_date(start_date),
                    "end_date": format_date(end_date)
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)} 