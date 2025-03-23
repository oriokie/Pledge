from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.fundraising_goal_group_member import FundraisingGoalGroupMember
from app.schemas.fundraising_goal_group_member import (
    FundraisingGoalGroupMemberCreate,
    FundraisingGoalGroupMemberUpdate
)

class CRUDFundraisingGoalGroupMember(
    CRUDBase[FundraisingGoalGroupMember, FundraisingGoalGroupMemberCreate, FundraisingGoalGroupMemberUpdate]
):
    def create(
        self, db: Session, *, obj_in: FundraisingGoalGroupMemberCreate
    ) -> FundraisingGoalGroupMember:
        db_obj = FundraisingGoalGroupMember(
            goal_id=obj_in.goal_id,
            group_id=obj_in.group_id,
            member_id=obj_in.member_id,
            target_amount=obj_in.target_amount,
            created_by=obj_in.created_by,
            updated_by=obj_in.created_by,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: FundraisingGoalGroupMember,
        obj_in: Union[FundraisingGoalGroupMemberUpdate, Dict[str, Any]]
    ) -> FundraisingGoalGroupMember:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_goal(
        self, db: Session, *, goal_id: int, skip: int = 0, limit: int = 100
    ) -> List[FundraisingGoalGroupMember]:
        return (
            db.query(self.model)
            .filter(FundraisingGoalGroupMember.goal_id == goal_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_group(
        self, db: Session, *, group_id: int, skip: int = 0, limit: int = 100
    ) -> List[FundraisingGoalGroupMember]:
        return (
            db.query(self.model)
            .filter(FundraisingGoalGroupMember.group_id == group_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_member(
        self, db: Session, *, member_id: int, skip: int = 0, limit: int = 100
    ) -> List[FundraisingGoalGroupMember]:
        return (
            db.query(self.model)
            .filter(FundraisingGoalGroupMember.member_id == member_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_member_target(
        self, db: Session, *, goal_id: int, group_id: int, member_id: int
    ) -> Optional[FundraisingGoalGroupMember]:
        return (
            db.query(self.model)
            .filter(
                FundraisingGoalGroupMember.goal_id == goal_id,
                FundraisingGoalGroupMember.group_id == group_id,
                FundraisingGoalGroupMember.member_id == member_id
            )
            .first()
        )

    def get_total_target_amount(
        self, db: Session, *, goal_id: int, group_id: int
    ) -> float:
        """Get total target amount for all members in a group for a fundraising goal"""
        result = db.query(func.sum(FundraisingGoalGroupMember.target_amount)).filter(
            FundraisingGoalGroupMember.goal_id == goal_id,
            FundraisingGoalGroupMember.group_id == group_id
        ).scalar()
        return result or 0.0

    def get_member_progress(
        self, db: Session, *, goal_id: int, group_id: int, member_id: int
    ) -> Dict[str, Any]:
        """Get progress summary for a member in a group for a fundraising goal"""
        member_target = self.get_member_target(
            db, goal_id=goal_id, group_id=group_id, member_id=member_id
        )
        if not member_target:
            return {
                "target_amount": 0.0,
                "contributed_amount": 0.0,
                "remaining_amount": 0.0,
                "progress_percentage": 0.0
            }
        
        # Get total contributions by the member for this goal and group
        contributed_amount = db.query(func.sum(FundraisingGoalContribution.amount)).filter(
            FundraisingGoalContribution.goal_id == goal_id,
            FundraisingGoalContribution.group_id == group_id,
            FundraisingGoalContribution.member_id == member_id
        ).scalar() or 0.0
        
        return {
            "target_amount": member_target.target_amount,
            "contributed_amount": contributed_amount,
            "remaining_amount": member_target.target_amount - contributed_amount,
            "progress_percentage": (contributed_amount / member_target.target_amount) * 100
        }

    def search(
        self,
        db: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[FundraisingGoalGroupMember]:
        """Search fundraising goal group members by goal ID, group ID, or member ID"""
        return (
            db.query(self.model)
            .filter(
                (FundraisingGoalGroupMember.goal_id == query) |
                (FundraisingGoalGroupMember.group_id == query) |
                (FundraisingGoalGroupMember.member_id == query)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

fundraising_goal_group_member = CRUDFundraisingGoalGroupMember(FundraisingGoalGroupMember) 