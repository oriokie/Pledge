from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.member import Member
from ..models.group import Group
from ..core.utils import validate_email, validate_phone_number
from ..schemas.member import MemberCreate, MemberUpdate

class MemberService:
    def __init__(self, db: Session):
        self.db = db

    def create_member(
        self,
        member_data: MemberCreate,
        group_id: int
    ) -> Dict[str, Any]:
        """Create a new member."""
        try:
            # Validate email and phone number
            if not validate_email(member_data.email):
                return {"status": "error", "message": "Invalid email format"}
            
            if not validate_phone_number(member_data.phone_number):
                return {"status": "error", "message": "Invalid phone number format"}

            # Check if group exists
            group = self.db.query(Group).filter(Group.id == group_id).first()
            if not group:
                return {"status": "error", "message": "Group not found"}

            # Check if email already exists in the group
            if self.db.query(Member).filter(
                Member.email == member_data.email,
                Member.group_id == group_id
            ).first():
                return {"status": "error", "message": "Email already registered in this group"}

            # Create member
            member = Member(
                email=member_data.email,
                full_name=member_data.full_name,
                phone_number=member_data.phone_number,
                group_id=group_id,
                role=member_data.role,
                is_active=member_data.is_active
            )
            self.db.add(member)
            self.db.commit()

            return {
                "status": "success",
                "member_id": member.id,
                "message": "Member created successfully"
            }
        except IntegrityError:
            return {"status": "error", "message": "Member already exists"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_member_by_id(
        self,
        member_id: int
    ) -> Dict[str, Any]:
        """Get member by ID."""
        try:
            member = self.db.query(Member).filter(Member.id == member_id).first()
            if not member:
                return {"status": "error", "message": "Member not found"}

            return {
                "status": "success",
                "member": {
                    "id": member.id,
                    "email": member.email,
                    "full_name": member.full_name,
                    "phone_number": member.phone_number,
                    "group_id": member.group_id,
                    "group_name": member.group.name,
                    "role": member.role,
                    "is_active": member.is_active,
                    "created_at": member.created_at.isoformat(),
                    "updated_at": member.updated_at.isoformat()
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_member(
        self,
        member_id: int,
        member_data: MemberUpdate
    ) -> Dict[str, Any]:
        """Update member information."""
        try:
            member = self.db.query(Member).filter(Member.id == member_id).first()
            if not member:
                return {"status": "error", "message": "Member not found"}

            # Update fields if provided
            if member_data.email and member_data.email != member.email:
                if not validate_email(member_data.email):
                    return {"status": "error", "message": "Invalid email format"}
                if self.db.query(Member).filter(
                    Member.email == member_data.email,
                    Member.group_id == member.group_id,
                    Member.id != member_id
                ).first():
                    return {"status": "error", "message": "Email already registered in this group"}
                member.email = member_data.email

            if member_data.full_name:
                member.full_name = member_data.full_name

            if member_data.phone_number and member_data.phone_number != member.phone_number:
                if not validate_phone_number(member_data.phone_number):
                    return {"status": "error", "message": "Invalid phone number format"}
                member.phone_number = member_data.phone_number

            if member_data.role:
                member.role = member_data.role

            if member_data.is_active is not None:
                member.is_active = member_data.is_active

            self.db.commit()

            return {
                "status": "success",
                "message": "Member updated successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_member(
        self,
        member_id: int
    ) -> Dict[str, Any]:
        """Delete a member."""
        try:
            member = self.db.query(Member).filter(Member.id == member_id).first()
            if not member:
                return {"status": "error", "message": "Member not found"}

            self.db.delete(member)
            self.db.commit()

            return {
                "status": "success",
                "message": "Member deleted successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_group_members(
        self,
        group_id: int,
        skip: int = 0,
        limit: int = 100,
        role: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Get list of members in a group with optional filters."""
        try:
            query = self.db.query(Member).filter(Member.group_id == group_id)

            if role:
                query = query.filter(Member.role == role)
            if is_active is not None:
                query = query.filter(Member.is_active == is_active)

            total_count = query.count()
            members = query.offset(skip).limit(limit).all()

            return {
                "status": "success",
                "total_count": total_count,
                "members": [
                    {
                        "id": member.id,
                        "email": member.email,
                        "full_name": member.full_name,
                        "phone_number": member.phone_number,
                        "role": member.role,
                        "is_active": member.is_active,
                        "created_at": member.created_at.isoformat(),
                        "updated_at": member.updated_at.isoformat()
                    }
                    for member in members
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_member_contributions(
        self,
        member_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> Dict[str, Any]:
        """Get member's contribution history."""
        try:
            member = self.db.query(Member).filter(Member.id == member_id).first()
            if not member:
                return {"status": "error", "message": "Member not found"}

            contributions = member.contributions.order_by(
                member.contributions.created_at.desc()
            ).offset(skip).limit(limit).all()

            total_amount = sum(c.amount for c in contributions)

            return {
                "status": "success",
                "total_amount": total_amount,
                "contributions": [
                    {
                        "id": c.id,
                        "amount": c.amount,
                        "status": c.status,
                        "created_at": c.created_at.isoformat(),
                        "payment_status": c.payment.status if c.payment else None
                    }
                    for c in contributions
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)} 