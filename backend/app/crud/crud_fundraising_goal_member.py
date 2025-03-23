from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.fundraising_goal_member import FundraisingGoalMember
from app.schemas.fundraising_goal_member import (
    FundraisingGoalMemberCreate,
    FundraisingGoalMemberUpdate
)

class CRUDFundraisingGoalMember(
    CRUDBase[FundraisingGoalMember, FundraisingGoalMemberCreate, FundraisingGoalMemberUpdate]
):
    def create(
        self, db: Session, *, obj_in: FundraisingGoalMemberCreate
    ) -> FundraisingGoalMember:
        db_obj = FundraisingGoalMember(
            goal_id=obj_in.goal_id,
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
        db_obj: FundraisingGoalMember,
        obj_in: Union[FundraisingGoalMemberUpdate, Dict[str, Any]]
    ) -> FundraisingGoalMember:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_goal(
        self, db: Session, *, goal_id: int, skip: int = 0, limit: int = 100
    ) -> List[FundraisingGoalMember]:
        return (
            db.query(self.model)
            .filter(FundraisingGoalMember.goal_id == goal_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_member(
        self, db: Session, *, member_id: int, skip: int = 0, limit: int = 100
    ) -> List[FundraisingGoalMember]:
        return (
            db.query(self.model)
            .filter(FundraisingGoalMember.member_id == member_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_member_target(
        self, db: Session, *, goal_id: int, member_id: int
    ) -> Optional[FundraisingGoalMember]:
        return (
            db.query(self.model)
            .filter(
                FundraisingGoalMember.goal_id == goal_id,
                FundraisingGoalMember.member_id == member_id
            )
            .first()
        )

    def get_total_target_amount(self, db: Session, *, goal_id: int) -> float:
        """Get total target amount for all members in a fundraising goal"""
        result = db.query(func.sum(FundraisingGoalMember.target_amount)).filter(
            FundraisingGoalMember.goal_id == goal_id
        ).scalar()
        return result or 0.0

    def get_member_progress(
        self, db: Session, *, goal_id: int, member_id: int
    ) -> Dict[str, Any]:
        """Get progress summary for a member in a fundraising goal"""
        member_target = self.get_member_target(db, goal_id=goal_id, member_id=member_id)
        if not member_target:
            return {
                "target_amount": 0.0,
                "contributed_amount": 0.0,
                "remaining_amount": 0.0,
                "progress_percentage": 0.0
            }
        
        # Get total contributions by the member for this goal
        contributed_amount = db.query(func.sum(FundraisingGoalContribution.amount)).filter(
            FundraisingGoalContribution.goal_id == goal_id,
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
    ) -> List[FundraisingGoalMember]:
        """Search fundraising goal members by goal ID or member ID"""
        return (
            db.query(self.model)
            .filter(
                (FundraisingGoalMember.goal_id == query) |
                (FundraisingGoalMember.member_id == query)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

fundraising_goal_member = CRUDFundraisingGoalMember(FundraisingGoalMember) 