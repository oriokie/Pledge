from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.fundraising_goal_progress import FundraisingGoalProgress
from app.schemas.fundraising_goal_progress import (
    FundraisingGoalProgressCreate,
    FundraisingGoalProgressUpdate
)

class CRUDFundraisingGoalProgress(
    CRUDBase[FundraisingGoalProgress, FundraisingGoalProgressCreate, FundraisingGoalProgressUpdate]
):
    def create(
        self, db: Session, *, obj_in: FundraisingGoalProgressCreate
    ) -> FundraisingGoalProgress:
        db_obj = FundraisingGoalProgress(
            goal_id=obj_in.goal_id,
            current_amount=obj_in.current_amount,
            target_amount=obj_in.target_amount,
            progress_percentage=obj_in.progress_percentage,
            created_at=datetime.utcnow(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: FundraisingGoalProgress,
        obj_in: Union[FundraisingGoalProgressUpdate, Dict[str, Any]]
    ) -> FundraisingGoalProgress:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_goal(
        self, db: Session, *, goal_id: int, skip: int = 0, limit: int = 100
    ) -> List[FundraisingGoalProgress]:
        return (
            db.query(self.model)
            .filter(FundraisingGoalProgress.goal_id == goal_id)
            .order_by(FundraisingGoalProgress.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_latest_progress(
        self, db: Session, *, goal_id: int
    ) -> Optional[FundraisingGoalProgress]:
        return (
            db.query(self.model)
            .filter(FundraisingGoalProgress.goal_id == goal_id)
            .order_by(FundraisingGoalProgress.created_at.desc())
            .first()
        )

    def get_progress_by_date_range(
        self,
        db: Session,
        *,
        goal_id: int,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        limit: int = 100
    ) -> List[FundraisingGoalProgress]:
        return (
            db.query(self.model)
            .filter(
                FundraisingGoalProgress.goal_id == goal_id,
                FundraisingGoalProgress.created_at >= start_date,
                FundraisingGoalProgress.created_at <= end_date
            )
            .order_by(FundraisingGoalProgress.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_progress_summary(
        self, db: Session, *, goal_id: int
    ) -> Dict[str, Any]:
        """Get summary of fundraising goal progress"""
        latest_progress = self.get_latest_progress(db, goal_id=goal_id)
        if not latest_progress:
            return {
                "current_amount": 0.0,
                "target_amount": 0.0,
                "progress_percentage": 0.0,
                "remaining_amount": 0.0,
                "last_updated": None
            }
        
        return {
            "current_amount": latest_progress.current_amount,
            "target_amount": latest_progress.target_amount,
            "progress_percentage": latest_progress.progress_percentage,
            "remaining_amount": latest_progress.target_amount - latest_progress.current_amount,
            "last_updated": latest_progress.created_at
        }

    def search(
        self,
        db: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[FundraisingGoalProgress]:
        """Search fundraising goal progress by goal ID"""
        return (
            db.query(self.model)
            .filter(FundraisingGoalProgress.goal_id == query)
            .order_by(FundraisingGoalProgress.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

fundraising_goal_progress = CRUDFundraisingGoalProgress(FundraisingGoalProgress) 