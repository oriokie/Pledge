from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate
from app.utils.member_code import generate_member_code

class CRUDMember(CRUDBase[Member, MemberCreate, MemberUpdate]):
    def get_by_phone(self, db: Session, *, phone: str) -> Optional[Member]:
        return db.query(Member).filter(Member.phone == phone).first()

    def get_by_code(self, db: Session, *, code: str) -> Optional[Member]:
        return db.query(Member).filter(Member.code == code).first()

    def get_by_alias(self, db: Session, *, alias: str) -> Optional[Member]:
        return db.query(Member).filter(Member.alias == alias).first()

    def create(self, db: Session, *, obj_in: MemberCreate) -> Member:
        # Generate unique member code
        code = generate_member_code(db)
        
        db_obj = Member(
            name=obj_in.name,
            phone=obj_in.phone,
            code=code,
            alias=obj_in.alias,
            address=obj_in.address,
            created_by=obj_in.created_by,
            updated_by=obj_in.created_by,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Member, obj_in: Union[MemberUpdate, Dict[str, Any]]
    ) -> Member:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_total_contributions(self, db: Session, *, member_id: int) -> float:
        """Get total contributions for a member"""
        result = db.query(func.sum(Member.contributions.any(Contribution.amount))).filter(
            Member.id == member_id
        ).scalar()
        return result or 0.0

    def get_total_pledges(self, db: Session, *, member_id: int) -> float:
        """Get total pledges for a member"""
        result = db.query(func.sum(Member.contributions.any(Contribution.amount))).filter(
            Member.id == member_id,
            Contribution.type == "pledge"
        ).scalar()
        return result or 0.0

    def search(
        self,
        db: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Member]:
        """Search members by name, phone, code, or alias"""
        return (
            db.query(self.model)
            .filter(
                (Member.name.ilike(f"%{query}%")) |
                (Member.phone.ilike(f"%{query}%")) |
                (Member.code.ilike(f"%{query}%")) |
                (Member.alias.ilike(f"%{query}%"))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

member = CRUDMember(Member) 