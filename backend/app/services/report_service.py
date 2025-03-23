from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from ..models.contribution import Contribution
from ..models.group import Group
from ..models.project import Project
from ..core.utils import format_currency

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_contribution_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        group_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get summary of contributions for a period."""
        try:
            query = self.db.query(
                func.count(Contribution.id).label("total_count"),
                func.sum(Contribution.amount).label("total_amount")
            ).filter(Contribution.status == "completed")

            if start_date:
                query = query.filter(Contribution.created_at >= start_date)
            if end_date:
                query = query.filter(Contribution.created_at <= end_date)
            if group_id:
                query = query.filter(Contribution.group_id == group_id)

            result = query.first()
            
            return {
                "status": "success",
                "summary": {
                    "total_count": result.total_count or 0,
                    "total_amount": format_currency(result.total_amount or 0),
                    "average_amount": format_currency(
                        (result.total_amount or 0) / (result.total_count or 1)
                    )
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
        """Get detailed report of member's contributions."""
        try:
            query = self.db.query(Contribution).filter(
                Contribution.member_id == member_id,
                Contribution.status == "completed"
            )

            if start_date:
                query = query.filter(Contribution.created_at >= start_date)
            if end_date:
                query = query.filter(Contribution.created_at <= end_date)

            contributions = query.all()
            
            total_amount = sum(c.amount for c in contributions)
            
            return {
                "status": "success",
                "report": {
                    "total_contributions": len(contributions),
                    "total_amount": format_currency(total_amount),
                    "contributions": [
                        {
                            "id": c.id,
                            "amount": format_currency(c.amount),
                            "description": c.description,
                            "created_at": c.created_at.isoformat(),
                            "group_name": c.group.name
                        }
                        for c in contributions
                    ]
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

            query = self.db.query(Contribution).filter(
                Contribution.group_id == group_id,
                Contribution.status == "completed"
            )

            if start_date:
                query = query.filter(Contribution.created_at >= start_date)
            if end_date:
                query = query.filter(Contribution.created_at <= end_date)

            contributions = query.all()
            
            total_amount = sum(c.amount for c in contributions)
            member_count = len(group.members)
            average_contribution = total_amount / member_count if member_count > 0 else 0

            return {
                "status": "success",
                "report": {
                    "group_name": group.name,
                    "total_contributions": len(contributions),
                    "total_amount": format_currency(total_amount),
                    "member_count": member_count,
                    "average_contribution": format_currency(average_contribution),
                    "target_amount": format_currency(group.target_amount),
                    "progress_percentage": (total_amount / group.target_amount * 100) if group.target_amount > 0 else 0
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_trend_analysis(
        self,
        days: int = 30,
        group_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get contribution trends over time."""
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)

            query = self.db.query(
                func.date(Contribution.created_at).label("date"),
                func.count(Contribution.id).label("count"),
                func.sum(Contribution.amount).label("amount")
            ).filter(
                Contribution.status == "completed",
                Contribution.created_at >= start_date,
                Contribution.created_at <= end_date
            )

            if group_id:
                query = query.filter(Contribution.group_id == group_id)

            results = query.group_by(func.date(Contribution.created_at)).all()

            return {
                "status": "success",
                "trends": [
                    {
                        "date": result.date.isoformat(),
                        "count": result.count,
                        "amount": format_currency(result.amount)
                    }
                    for result in results
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)} 