from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.pledge import Pledge, PledgeStatus
from ..models.member import Member
from ..models.group import Group
from ..models.project import Project
from ..schemas.pledge import PledgeCreate, PledgeUpdate
from ..core.utils import format_currency

class PledgeService:
    def __init__(self, db: Session):
        self.db = db

    def create_pledge(
        self,
        pledge_data: PledgeCreate,
        created_by_id: int
    ) -> Dict[str, Any]:
        """Create a new pledge."""
        try:
            # Validate member
            member = self.db.query(Member).filter(Member.id == pledge_data.member_id).first()
            if not member:
                return {"status": "error", "message": "Member not found"}

            # Validate project
            project = self.db.query(Project).filter(Project.id == pledge_data.project_id).first()
            if not project:
                return {"status": "error", "message": "Project not found"}

            # Validate group if provided
            if pledge_data.group_id:
                group = self.db.query(Group).filter(Group.id == pledge_data.group_id).first()
                if not group:
                    return {"status": "error", "message": "Group not found"}
                # Check if member belongs to the group
                if member not in group.members:
                    return {"status": "error", "message": "Member does not belong to this group"}

            # Create pledge
            pledge = Pledge(
                **pledge_data.dict(),
                created_by_id=created_by_id,
                status=PledgeStatus.PENDING
            )
            self.db.add(pledge)
            self.db.commit()
            self.db.refresh(pledge)

            return {
                "status": "success",
                "pledge_id": pledge.id,
                "message": "Pledge created successfully"
            }
        except IntegrityError:
            return {"status": "error", "message": "Pledge already exists"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_pledge_by_id(
        self,
        pledge_id: int
    ) -> Dict[str, Any]:
        """Get pledge by ID."""
        try:
            pledge = self.db.query(Pledge).filter(Pledge.id == pledge_id).first()
            if not pledge:
                return {"status": "error", "message": "Pledge not found"}

            return {
                "status": "success",
                "pledge": {
                    "id": pledge.id,
                    "member_name": pledge.member.full_name,
                    "group_name": pledge.group.name if pledge.group else None,
                    "project_name": pledge.project.name,
                    "amount": format_currency(pledge.amount),
                    "pledge_date": pledge.pledge_date.isoformat(),
                    "due_date": pledge.due_date.isoformat(),
                    "status": pledge.status,
                    "description": pledge.description,
                    "created_at": pledge.created_at.isoformat(),
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_pledge(
        self,
        pledge_id: int,
        pledge_data: PledgeUpdate
    ) -> Dict[str, Any]:
        """Update pledge information."""
        try:
            pledge = self.db.query(Pledge).filter(Pledge.id == pledge_id).first()
            if not pledge:
                return {"status": "error", "message": "Pledge not found"}

            # Update fields if provided
            for field, value in pledge_data.dict(exclude_unset=True).items():
                setattr(pledge, field, value)

            self.db.commit()

            return {
                "status": "success",
                "message": "Pledge updated successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_pledge(
        self,
        pledge_id: int
    ) -> Dict[str, Any]:
        """Delete a pledge."""
        try:
            pledge = self.db.query(Pledge).filter(Pledge.id == pledge_id).first()
            if not pledge:
                return {"status": "error", "message": "Pledge not found"}

            self.db.delete(pledge)
            self.db.commit()

            return {
                "status": "success",
                "message": "Pledge deleted successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_member_pledges(
        self,
        member_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get member's pledge history."""
        try:
            query = self.db.query(Pledge).filter(Pledge.member_id == member_id)

            if status:
                query = query.filter(Pledge.status == status)

            total_count = query.count()
            pledges = query.order_by(Pledge.created_at.desc()).offset(skip).limit(limit).all()

            total_amount = sum(p.amount for p in pledges)

            return {
                "status": "success",
                "total_count": total_count,
                "total_amount": format_currency(total_amount),
                "pledges": [
                    {
                        "id": p.id,
                        "group_name": p.group.name if p.group else None,
                        "project_name": p.project.name,
                        "amount": format_currency(p.amount),
                        "pledge_date": p.pledge_date.isoformat(),
                        "due_date": p.due_date.isoformat(),
                        "status": p.status,
                        "description": p.description,
                        "created_at": p.created_at.isoformat(),
                    }
                    for p in pledges
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_group_pledges(
        self,
        group_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get group's pledge history."""
        try:
            query = self.db.query(Pledge).filter(Pledge.group_id == group_id)

            if status:
                query = query.filter(Pledge.status == status)

            total_count = query.count()
            pledges = query.order_by(Pledge.created_at.desc()).offset(skip).limit(limit).all()

            total_amount = sum(p.amount for p in pledges)

            return {
                "status": "success",
                "total_count": total_count,
                "total_amount": format_currency(total_amount),
                "pledges": [
                    {
                        "id": p.id,
                        "member_name": p.member.full_name,
                        "project_name": p.project.name,
                        "amount": format_currency(p.amount),
                        "pledge_date": p.pledge_date.isoformat(),
                        "due_date": p.due_date.isoformat(),
                        "status": p.status,
                        "description": p.description,
                        "created_at": p.created_at.isoformat(),
                    }
                    for p in pledges
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_pledges(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        member_id: Optional[int] = None,
        group_id: Optional[int] = None,
        project_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get list of pledges with optional filters."""
        try:
            query = self.db.query(Pledge)

            if status:
                query = query.filter(Pledge.status == status)
            if member_id:
                query = query.filter(Pledge.member_id == member_id)
            if group_id:
                query = query.filter(Pledge.group_id == group_id)
            if project_id:
                query = query.filter(Pledge.project_id == project_id)

            total_count = query.count()
            pledges = query.order_by(Pledge.created_at.desc()).offset(skip).limit(limit).all()

            total_amount = sum(p.amount for p in pledges)

            return {
                "status": "success",
                "total_count": total_count,
                "total_amount": format_currency(total_amount),
                "pledges": [
                    {
                        "id": p.id,
                        "member_name": p.member.full_name,
                        "group_name": p.group.name if p.group else None,
                        "project_name": p.project.name,
                        "amount": format_currency(p.amount),
                        "pledge_date": p.pledge_date.isoformat(),
                        "due_date": p.due_date.isoformat(),
                        "status": p.status,
                        "description": p.description,
                        "created_at": p.created_at.isoformat(),
                    }
                    for p in pledges
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_pledge(self, pledge_id: int) -> Optional[Pledge]:
        """
        Get a pledge by ID.
        """
        return self.db.query(Pledge).filter(Pledge.id == pledge_id).first()

    def update_pledge(
        self,
        pledge: Pledge,
        pledge_in: PledgeUpdate
    ) -> Pledge:
        """
        Update a pledge.
        """
        update_data = pledge_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(pledge, field, value)
        
        self.db.add(pledge)
        self.db.commit()
        self.db.refresh(pledge)
        return pledge

    def delete_pledge(self, pledge: Pledge) -> Pledge:
        """
        Delete a pledge.
        """
        self.db.delete(pledge)
        self.db.commit()
        return pledge 