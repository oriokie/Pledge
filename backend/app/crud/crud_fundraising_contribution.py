from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.fundraising_contribution import FundraisingContribution
from app.schemas.fundraising_contribution import (
    FundraisingContributionCreate,
    FundraisingContributionUpdate
)

class CRUDFundraisingContribution(
    CRUDBase[FundraisingContribution, FundraisingContributionCreate, FundraisingContributionUpdate]
):
    def create(
        self, db: Session, *, obj_in: FundraisingContributionCreate
    ) -> FundraisingContribution:
        db_obj = FundraisingContribution(
            fundraising_id=obj_in.fundraising_id,
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
        db_obj: FundraisingContribution,
        obj_in: Union[FundraisingContributionUpdate, Dict[str, Any]]
    ) -> FundraisingContribution:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_fundraising(
        self, db: Session, *, fundraising_id: int, skip: int = 0, limit: int = 100
    ) -> List[FundraisingContribution]:
        return (
            db.query(self.model)
            .filter(FundraisingContribution.fundraising_id == fundraising_id)
            .order_by(FundraisingContribution.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_member(
        self, db: Session, *, member_id: int, skip: int = 0, limit: int = 100
    ) -> List[FundraisingContribution]:
        return (
            db.query(self.model)
            .filter(FundraisingContribution.member_id == member_id)
            .order_by(FundraisingContribution.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_group(
        self, db: Session, *, group_id: int, skip: int = 0, limit: int = 100
    ) -> List[FundraisingContribution]:
        return (
            db.query(self.model)
            .filter(FundraisingContribution.group_id == group_id)
            .order_by(FundraisingContribution.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_total_contributions(self, db: Session, *, fundraising_id: int) -> float:
        """Get total contributions for a fundraising activity"""
        result = db.query(func.sum(FundraisingContribution.amount)).filter(
            FundraisingContribution.fundraising_id == fundraising_id
        ).scalar()
        return result or 0.0

    def get_member_contributions(
        self, db: Session, *, member_id: int, fundraising_id: int
    ) -> float:
        """Get total contributions by a member for a fundraising activity"""
        result = db.query(func.sum(FundraisingContribution.amount)).filter(
            FundraisingContribution.member_id == member_id,
            FundraisingContribution.fundraising_id == fundraising_id
        ).scalar()
        return result or 0.0

    def get_group_contributions(
        self, db: Session, *, group_id: int, fundraising_id: int
    ) -> float:
        """Get total contributions by a group for a fundraising activity"""
        result = db.query(func.sum(FundraisingContribution.amount)).filter(
            FundraisingContribution.group_id == group_id,
            FundraisingContribution.fundraising_id == fundraising_id
        ).scalar()
        return result or 0.0

    def search(
        self,
        db: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[FundraisingContribution]:
        """Search fundraising contributions by reference number or payment method"""
        return (
            db.query(self.model)
            .filter(
                (FundraisingContribution.reference_number.ilike(f"%{query}%")) |
                (FundraisingContribution.payment_method.ilike(f"%{query}%"))
            )
            .order_by(FundraisingContribution.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

fundraising_contribution = CRUDFundraisingContribution(FundraisingContribution) 