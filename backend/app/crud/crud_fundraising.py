from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.fundraising import Fundraising
from app.schemas.fundraising import FundraisingCreate, FundraisingUpdate

class CRUDFundraising(CRUDBase[Fundraising, FundraisingCreate, FundraisingUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Fundraising]:
        return db.query(Fundraising).filter(Fundraising.name == name).first()

    def create(self, db: Session, *, obj_in: FundraisingCreate) -> Fundraising:
        db_obj = Fundraising(
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
        self, db: Session, *, db_obj: Fundraising, obj_in: Union[FundraisingUpdate, Dict[str, Any]]
    ) -> Fundraising:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_active_fundraising(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Fundraising]:
        return (
            db.query(self.model)
            .filter(Fundraising.status == "active")
            .order_by(Fundraising.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_completed_fundraising(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Fundraising]:
        return (
            db.query(self.model)
            .filter(Fundraising.status == "completed")
            .order_by(Fundraising.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_total_raised(self, db: Session, *, fundraising_id: int) -> float:
        """Get total amount raised for a fundraising activity"""
        result = db.query(func.sum(Fundraising.contributions.any(Contribution.amount))).filter(
            Fundraising.id == fundraising_id,
            Contribution.type == "contribution"
        ).scalar()
        return result or 0.0

    def get_fundraising_summary(
        self, db: Session, *, fundraising_id: int
    ) -> Dict[str, float]:
        """Get summary of fundraising activity"""
        total_raised = self.get_total_raised(db, fundraising_id=fundraising_id)
        fundraising = self.get(db, id=fundraising_id)
        
        return {
            "total_raised": total_raised,
            "target_amount": fundraising.target_amount,
            "remaining_amount": fundraising.target_amount - total_raised,
            "progress_percentage": (total_raised / fundraising.target_amount) * 100
        }

    def search(
        self,
        db: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Fundraising]:
        """Search fundraising activities by name or description"""
        return (
            db.query(self.model)
            .filter(
                (Fundraising.name.ilike(f"%{query}%")) |
                (Fundraising.description.ilike(f"%{query}%"))
            )
            .order_by(Fundraising.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

fundraising = CRUDFundraising(Fundraising) 