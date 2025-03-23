from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.group import Group
from ..models.member import Member
from ..models.contribution import Contribution
from ..core.utils import format_currency
from ..schemas.group import GroupCreate, GroupUpdate

class GroupService:
    def __init__(self, db: Session):
        self.db = db

    def create_group(
        self,
        group_data: GroupCreate
    ) -> Dict[str, Any]:
        """Create a new group."""
        try:
            # Check if group name already exists
            if self.db.query(Group).filter(Group.name == group_data.name).first():
                return {"status": "error", "message": "Group name already exists"}

            # Create group
            group = Group(
                name=group_data.name,
                description=group_data.description,
                target_amount=group_data.target_amount,
                start_date=group_data.start_date,
                end_date=group_data.end_date,
                is_active=group_data.is_active
            )
            self.db.add(group)
            self.db.commit()

            return {
                "status": "success",
                "group_id": group.id,
                "message": "Group created successfully"
            }
        except IntegrityError:
            return {"status": "error", "message": "Group already exists"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_group_by_id(
        self,
        group_id: int
    ) -> Dict[str, Any]:
        """Get group by ID."""
        try:
            group = self.db.query(Group).filter(Group.id == group_id).first()
            if not group:
                return {"status": "error", "message": "Group not found"}

            # Calculate total contributions
            total_contributions = sum(c.amount for c in group.contributions if c.status == "completed")
            progress_percentage = (total_contributions / group.target_amount * 100) if group.target_amount > 0 else 0

            return {
                "status": "success",
                "group": {
                    "id": group.id,
                    "name": group.name,
                    "description": group.description,
                    "target_amount": format_currency(group.target_amount),
                    "total_contributions": format_currency(total_contributions),
                    "progress_percentage": progress_percentage,
                    "start_date": group.start_date.isoformat() if group.start_date else None,
                    "end_date": group.end_date.isoformat() if group.end_date else None,
                    "is_active": group.is_active,
                    "member_count": len(group.members),
                    "created_at": group.created_at.isoformat(),
                    "updated_at": group.updated_at.isoformat()
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_group(
        self,
        group_id: int,
        group_data: GroupUpdate
    ) -> Dict[str, Any]:
        """Update group information."""
        try:
            group = self.db.query(Group).filter(Group.id == group_id).first()
            if not group:
                return {"status": "error", "message": "Group not found"}

            # Update fields if provided
            if group_data.name and group_data.name != group.name:
                if self.db.query(Group).filter(
                    Group.name == group_data.name,
                    Group.id != group_id
                ).first():
                    return {"status": "error", "message": "Group name already exists"}
                group.name = group_data.name

            if group_data.description:
                group.description = group_data.description

            if group_data.target_amount:
                group.target_amount = group_data.target_amount

            if group_data.start_date:
                group.start_date = group_data.start_date

            if group_data.end_date:
                group.end_date = group_data.end_date

            if group_data.is_active is not None:
                group.is_active = group_data.is_active

            self.db.commit()

            return {
                "status": "success",
                "message": "Group updated successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_group(
        self,
        group_id: int
    ) -> Dict[str, Any]:
        """Delete a group."""
        try:
            group = self.db.query(Group).filter(Group.id == group_id).first()
            if not group:
                return {"status": "error", "message": "Group not found"}

            # Check if group has members or contributions
            if group.members or group.contributions:
                return {"status": "error", "message": "Cannot delete group with members or contributions"}

            self.db.delete(group)
            self.db.commit()

            return {
                "status": "success",
                "message": "Group deleted successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_groups(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Get list of groups with optional filters."""
        try:
            query = self.db.query(Group)

            if is_active is not None:
                query = query.filter(Group.is_active == is_active)

            total_count = query.count()
            groups = query.offset(skip).limit(limit).all()

            return {
                "status": "success",
                "total_count": total_count,
                "groups": [
                    {
                        "id": group.id,
                        "name": group.name,
                        "description": group.description,
                        "target_amount": format_currency(group.target_amount),
                        "total_contributions": format_currency(
                            sum(c.amount for c in group.contributions if c.status == "completed")
                        ),
                        "start_date": group.start_date.isoformat() if group.start_date else None,
                        "end_date": group.end_date.isoformat() if group.end_date else None,
                        "is_active": group.is_active,
                        "member_count": len(group.members),
                        "created_at": group.created_at.isoformat(),
                        "updated_at": group.updated_at.isoformat()
                    }
                    for group in groups
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
            group = self.db.query(Group).filter(Group.id == group_id).first()
            if not group:
                return {"status": "error", "message": "Group not found"}

            query = group.contributions

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
                        "status": c.status,
                        "created_at": c.created_at.isoformat(),
                        "payment_status": c.payment.status if c.payment else None
                    }
                    for c in contributions
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)} 