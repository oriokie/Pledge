from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.fundraising_goal import FundraisingGoal
from app.schemas.fundraising_goal import FundraisingGoalCreate, FundraisingGoalUpdate

class CRUDFundraisingGoal(CRUDBase[FundraisingGoal, FundraisingGoalCreate, FundraisingGoalUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[FundraisingGoal]:
        return db.query(FundraisingGoal).filter(FundraisingGoal.name == name).first()

    def create(self, db: Session, *, obj_in: FundraisingGoalCreate) -> FundraisingGoal:
        db_obj = FundraisingGoal(
            name=obj_in.name,
            description=obj_in.description,
            target_amount=obj_in.target_amount,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            status=obj_in.status,
            created_by=obj_in.created_by,
            updated_by=obj_in.created_by,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: FundraisingGoal, obj_in: Union[FundraisingGoalUpdate, Dict[str, Any]]
    ) -> FundraisingGoal:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_active_goals(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[FundraisingGoal]:
        return (
            db.query(self.model)
            .filter(FundraisingGoal.status == "active")
            .order_by(FundraisingGoal.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_completed_goals(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[FundraisingGoal]:
        return (
            db.query(self.model)
            .filter(FundraisingGoal.status == "completed")
            .order_by(FundraisingGoal.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_total_raised(self, db: Session, *, goal_id: int) -> float:
        """Get total amount raised for a fundraising goal"""
        result = db.query(func.sum(FundraisingGoal.contributions.any(Contribution.amount))).filter(
            FundraisingGoal.id == goal_id,
            Contribution.type == "contribution"
        ).scalar()
        return result or 0.0

    def get_goal_summary(
        self, db: Session, *, goal_id: int
    ) -> Dict[str, float]:
        """Get summary of fundraising goal"""
        total_raised = self.get_total_raised(db, goal_id=goal_id)
        goal = self.get(db, id=goal_id)
        
        return {
            "total_raised": total_raised,
            "target_amount": goal.target_amount,
            "remaining_amount": goal.target_amount - total_raised,
            "progress_percentage": (total_raised / goal.target_amount) * 100
        }

    def search(
        self,
        db: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[FundraisingGoal]:
        """Search fundraising goals by name or description"""
        return (
            db.query(self.model)
            .filter(
                (FundraisingGoal.name.ilike(f"%{query}%")) |
                (FundraisingGoal.description.ilike(f"%{query}%"))
            )
            .order_by(FundraisingGoal.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

fundraising_goal = CRUDFundraisingGoal(FundraisingGoal) 