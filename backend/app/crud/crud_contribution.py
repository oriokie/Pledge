from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.contribution import Contribution
from app.schemas.contribution import ContributionCreate, ContributionUpdate

class CRUDContribution(CRUDBase[Contribution, ContributionCreate, ContributionUpdate]):
    def create(self, db: Session, *, obj_in: ContributionCreate) -> Contribution:
        db_obj = Contribution(
            member_id=obj_in.member_id,
            project_id=obj_in.project_id,
            group_id=obj_in.group_id,
            amount=obj_in.amount,
            type=obj_in.type,
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
        self, db: Session, *, db_obj: Contribution, obj_in: Union[ContributionUpdate, Dict[str, Any]]
    ) -> Contribution:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_member(
        self, db: Session, *, member_id: int, skip: int = 0, limit: int = 100
    ) -> List[Contribution]:
        return (
            db.query(self.model)
            .filter(Contribution.member_id == member_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_project(
        self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100
    ) -> List[Contribution]:
        return (
            db.query(self.model)
            .filter(Contribution.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_group(
        self, db: Session, *, group_id: int, skip: int = 0, limit: int = 100
    ) -> List[Contribution]:
        return (
            db.query(self.model)
            .filter(Contribution.group_id == group_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_total_contributions(self, db: Session) -> float:
        """Get total contributions across all projects"""
        result = db.query(func.sum(Contribution.amount)).filter(
            Contribution.type == "contribution"
        ).scalar()
        return result or 0.0

    def get_total_pledges(self, db: Session) -> float:
        """Get total pledges across all projects"""
        result = db.query(func.sum(Contribution.amount)).filter(
            Contribution.type == "pledge"
        ).scalar()
        return result or 0.0

    def get_project_summary(
        self, db: Session, *, project_id: int
    ) -> Dict[str, float]:
        """Get summary of contributions and pledges for a project"""
        total_contributions = db.query(func.sum(Contribution.amount)).filter(
            Contribution.project_id == project_id,
            Contribution.type == "contribution"
        ).scalar() or 0.0

        total_pledges = db.query(func.sum(Contribution.amount)).filter(
            Contribution.project_id == project_id,
            Contribution.type == "pledge"
        ).scalar() or 0.0

        return {
            "total_contributions": total_contributions,
            "total_pledges": total_pledges,
            "remaining_balance": total_pledges - total_contributions
        }

    def search(
        self,
        db: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Contribution]:
        """Search contributions by reference number or payment method"""
        return (
            db.query(self.model)
            .filter(
                (Contribution.reference_number.ilike(f"%{query}%")) |
                (Contribution.payment_method.ilike(f"%{query}%"))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

contribution = CRUDContribution(Contribution) 