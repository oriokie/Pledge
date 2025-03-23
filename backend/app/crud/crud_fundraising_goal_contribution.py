from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.fundraising_goal_contribution import FundraisingGoalContribution
from app.schemas.fundraising_goal_contribution import (
    FundraisingGoalContributionCreate,
    FundraisingGoalContributionUpdate
)

class CRUDFundraisingGoalContribution(
    CRUDBase[FundraisingGoalContribution, FundraisingGoalContributionCreate, FundraisingGoalContributionUpdate]
):
    def create(
        self, db: Session, *, obj_in: FundraisingGoalContributionCreate
    ) -> FundraisingGoalContribution:
        db_obj = FundraisingGoalContribution(
            goal_id=obj_in.goal_id,
            member_id=obj_in.member_id,
            group_id=obj_in.group_id,
            amount=obj_in.amount,
            payment_method=obj_in.payment_method,
            reference_number=obj_in.reference_number,
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
        db_obj: FundraisingGoalContribution,
        obj_in: Union[FundraisingGoalContributionUpdate, Dict[str, Any]]
    ) -> FundraisingGoalContribution:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_goal(
        self, db: Session, *, goal_id: int, skip: int = 0, limit: int = 100
    ) -> List[FundraisingGoalContribution]:
        return (
            db.query(self.model)
            .filter(FundraisingGoalContribution.goal_id == goal_id)
            .order_by(FundraisingGoalContribution.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_member(
        self, db: Session, *, member_id: int, skip: int = 0, limit: int = 100
    ) -> List[FundraisingGoalContribution]:
        return (
            db.query(self.model)
            .filter(FundraisingGoalContribution.member_id == member_id)
            .order_by(FundraisingGoalContribution.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_group(
        self, db: Session, *, group_id: int, skip: int = 0, limit: int = 100
    ) -> List[FundraisingGoalContribution]:
        return (
            db.query(self.model)
            .filter(FundraisingGoalContribution.group_id == group_id)
            .order_by(FundraisingGoalContribution.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_total_contributions(self, db: Session, *, goal_id: int) -> float:
        """Get total contributions for a fundraising goal"""
        result = db.query(func.sum(FundraisingGoalContribution.amount)).filter(
            FundraisingGoalContribution.goal_id == goal_id
        ).scalar()
        return result or 0.0

    def get_member_contributions(
        self, db: Session, *, member_id: int, goal_id: int
    ) -> float:
        """Get total contributions by a member for a fundraising goal"""
        result = db.query(func.sum(FundraisingGoalContribution.amount)).filter(
            FundraisingGoalContribution.member_id == member_id,
            FundraisingGoalContribution.goal_id == goal_id
        ).scalar()
        return result or 0.0

    def get_group_contributions(
        self, db: Session, *, group_id: int, goal_id: int
    ) -> float:
        """Get total contributions by a group for a fundraising goal"""
        result = db.query(func.sum(FundraisingGoalContribution.amount)).filter(
            FundraisingGoalContribution.group_id == group_id,
            FundraisingGoalContribution.goal_id == goal_id
        ).scalar()
        return result or 0.0

    def search(
        self,
        db: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[FundraisingGoalContribution]:
        """Search fundraising goal contributions by reference number or payment method"""
        return (
            db.query(self.model)
            .filter(
                (FundraisingGoalContribution.reference_number.ilike(f"%{query}%")) |
                (FundraisingGoalContribution.payment_method.ilike(f"%{query}%"))
            )
            .order_by(FundraisingGoalContribution.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

fundraising_goal_contribution = CRUDFundraisingGoalContribution(FundraisingGoalContribution) 