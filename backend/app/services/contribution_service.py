from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.contribution import Contribution
from ..models.member import Member
from ..models.group import Group
from ..core.utils import format_currency
from ..schemas.contribution import ContributionCreate, ContributionUpdate
from .payment_service import PaymentService

class ContributionService:
    def __init__(self, db: Session):
        self.db = db
        self.payment_service = PaymentService(db)

    def create_contribution(
        self,
        contribution_data: ContributionCreate,
        member_id: int
    ) -> Dict[str, Any]:
        """Create a new contribution."""
        try:
            # Validate member
            member = self.db.query(Member).filter(Member.id == member_id).first()
            if not member:
                return {"status": "error", "message": "Member not found"}

            # Validate group
            group = self.db.query(Group).filter(Group.id == contribution_data.group_id).first()
            if not group:
                return {"status": "error", "message": "Group not found"}

            # Check if member belongs to the group
            if member.group_id != contribution_data.group_id:
                return {"status": "error", "message": "Member does not belong to this group"}

            # Create contribution
            contribution = Contribution(
                member_id=member_id,
                group_id=contribution_data.group_id,
                amount=contribution_data.amount,
                description=contribution_data.description,
                status="pending"
            )
            self.db.add(contribution)
            self.db.commit()

            # Create payment intent
            payment_result = self.payment_service.create_payment_intent(
                amount=contribution_data.amount,
                metadata={
                    "contribution_id": contribution.id,
                    "member_id": member_id,
                    "group_id": contribution_data.group_id
                }
            )

            if payment_result["status"] == "error":
                contribution.status = "failed"
                contribution.error_message = payment_result["message"]
                self.db.commit()
                return payment_result

            return {
                "status": "success",
                "contribution_id": contribution.id,
                "client_secret": payment_result["client_secret"],
                "message": "Contribution created successfully"
            }
        except IntegrityError:
            return {"status": "error", "message": "Contribution already exists"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_contribution_by_id(
        self,
        contribution_id: int
    ) -> Dict[str, Any]:
        """Get contribution by ID."""
        try:
            contribution = self.db.query(Contribution).filter(Contribution.id == contribution_id).first()
            if not contribution:
                return {"status": "error", "message": "Contribution not found"}

            return {
                "status": "success",
                "contribution": {
                    "id": contribution.id,
                    "member_name": contribution.member.full_name,
                    "group_name": contribution.group.name,
                    "amount": format_currency(contribution.amount),
                    "description": contribution.description,
                    "status": contribution.status,
                    "error_message": contribution.error_message,
                    "created_at": contribution.created_at.isoformat(),
                    "payment_status": contribution.payment.status if contribution.payment else None,
                    "payment_method": contribution.payment.payment_method if contribution.payment else None
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_contribution(
        self,
        contribution_id: int,
        contribution_data: ContributionUpdate
    ) -> Dict[str, Any]:
        """Update contribution information."""
        try:
            contribution = self.db.query(Contribution).filter(Contribution.id == contribution_id).first()
            if not contribution:
                return {"status": "error", "message": "Contribution not found"}

            # Only allow updating description for completed contributions
            if contribution.status == "completed" and contribution_data.amount:
                return {"status": "error", "message": "Cannot update amount of completed contribution"}

            # Update fields if provided
            if contribution_data.amount and contribution.status != "completed":
                contribution.amount = contribution_data.amount

            if contribution_data.description:
                contribution.description = contribution_data.description

            self.db.commit()

            return {
                "status": "success",
                "message": "Contribution updated successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def cancel_contribution(
        self,
        contribution_id: int
    ) -> Dict[str, Any]:
        """Cancel a contribution."""
        try:
            contribution = self.db.query(Contribution).filter(Contribution.id == contribution_id).first()
            if not contribution:
                return {"status": "error", "message": "Contribution not found"}

            if contribution.status == "completed":
                return {"status": "error", "message": "Cannot cancel completed contribution"}

            contribution.status = "cancelled"
            contribution.error_message = "Contribution cancelled by user"
            self.db.commit()

            return {
                "status": "success",
                "message": "Contribution cancelled successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_member_contributions(
        self,
        member_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get member's contribution history."""
        try:
            query = self.db.query(Contribution).filter(Contribution.member_id == member_id)

            if status:
                query = query.filter(Contribution.status == status)

            total_count = query.count()
            contributions = query.order_by(Contribution.created_at.desc()).offset(skip).limit(limit).all()

            total_amount = sum(c.amount for c in contributions if c.status == "completed")

            return {
                "status": "success",
                "total_count": total_count,
                "total_amount": format_currency(total_amount),
                "contributions": [
                    {
                        "id": c.id,
                        "group_name": c.group.name,
                        "amount": format_currency(c.amount),
                        "description": c.description,
                        "status": c.status,
                        "created_at": c.created_at.isoformat(),
                        "payment_status": c.payment.status if c.payment else None
                    }
                    for c in contributions
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_group_contributions(
        self,
        group_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get group's contribution history."""
        try:
            query = self.db.query(Contribution).filter(Contribution.group_id == group_id)

            if status:
                query = query.filter(Contribution.status == status)

            total_count = query.count()
            contributions = query.order_by(Contribution.created_at.desc()).offset(skip).limit(limit).all()

            total_amount = sum(c.amount for c in contributions if c.status == "completed")

            return {
                "status": "success",
                "total_count": total_count,
                "total_amount": format_currency(total_amount),
                "contributions": [
                    {
                        "id": c.id,
                        "member_name": c.member.full_name,
                        "amount": format_currency(c.amount),
                        "description": c.description,
                        "status": c.status,
                        "created_at": c.created_at.isoformat(),
                        "payment_status": c.payment.status if c.payment else None
                    }
                    for c in contributions
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)} 