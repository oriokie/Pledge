from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.fundraising_goal_group import FundraisingGoalGroup
from app.schemas.fundraising_goal_group import (
    FundraisingGoalGroupCreate,
    FundraisingGoalGroupUpdate
)

class CRUDFundraisingGoalGroup(
    CRUDBase[FundraisingGoalGroup, FundraisingGoalGroupCreate, FundraisingGoalGroupUpdate]
):
    def create(
        self, db: Session, *, obj_in: FundraisingGoalGroupCreate
    ) -> FundraisingGoalGroup:
        db_obj = FundraisingGoalGroup(
            goal_id=obj_in.goal_id,
            group_id=obj_in.group_id,
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
        db_obj: FundraisingGoalGroup,
        obj_in: Union[FundraisingGoalGroupUpdate, Dict[str, Any]]
    ) -> FundraisingGoalGroup:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_goal(
        self, db: Session, *, goal_id: int, skip: int = 0, limit: int = 100
    ) -> List[FundraisingGoalGroup]:
        return (
            db.query(self.model)
            .filter(FundraisingGoalGroup.goal_id == goal_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_group(
        self, db: Session, *, group_id: int, skip: int = 0, limit: int = 100
    ) -> List[FundraisingGoalGroup]:
        return (
            db.query(self.model)
            .filter(FundraisingGoalGroup.group_id == group_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_group_target(
        self, db: Session, *, goal_id: int, group_id: int
    ) -> Optional[FundraisingGoalGroup]:
        return (
            db.query(self.model)
            .filter(
                FundraisingGoalGroup.goal_id == goal_id,
                FundraisingGoalGroup.group_id == group_id
            )
            .first()
        )

    def get_total_target_amount(self, db: Session, *, goal_id: int) -> float:
        """Get total target amount for all groups in a fundraising goal"""
        result = db.query(func.sum(FundraisingGoalGroup.target_amount)).filter(
            FundraisingGoalGroup.goal_id == goal_id
        ).scalar()
        return result or 0.0

    def get_group_progress(
        self, db: Session, *, goal_id: int, group_id: int
    ) -> Dict[str, Any]:
        """Get progress summary for a group in a fundraising goal"""
        group_target = self.get_group_target(db, goal_id=goal_id, group_id=group_id)
        if not group_target:
            return {
                "target_amount": 0.0,
                "contributed_amount": 0.0,
                "remaining_amount": 0.0,
                "progress_percentage": 0.0
            }
        
        # Get total contributions by the group for this goal
        contributed_amount = db.query(func.sum(FundraisingGoalContribution.amount)).filter(
            FundraisingGoalContribution.goal_id == goal_id,
            FundraisingGoalContribution.group_id == group_id
        ).scalar() or 0.0
        
        return {
            "target_amount": group_target.target_amount,
            "contributed_amount": contributed_amount,
            "remaining_amount": group_target.target_amount - contributed_amount,
            "progress_percentage": (contributed_amount / group_target.target_amount) * 100
        }

    def search(
        self,
        db: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[FundraisingGoalGroup]:
        """Search fundraising goal groups by goal ID or group ID"""
        return (
            db.query(self.model)
            .filter(
                (FundraisingGoalGroup.goal_id == query) |
                (FundraisingGoalGroup.group_id == query)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

fundraising_goal_group = CRUDFundraisingGoalGroup(FundraisingGoalGroup) 