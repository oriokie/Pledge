from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate

class CRUDGroup(CRUDBase[Group, GroupCreate, GroupUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Group]:
        return db.query(Group).filter(Group.name == name).first()

    def create(self, db: Session, *, obj_in: GroupCreate) -> Group:
        db_obj = Group(
            name=obj_in.name,
            description=obj_in.description,
            created_by=obj_in.created_by,
            updated_by=obj_in.created_by,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: Group, obj_in: Union[GroupUpdate, Dict[str, Any]]
    ) -> Group:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_total_contributions(self, db: Session, *, group_id: int) -> float:
        """Get total contributions for a group"""
        result = db.query(func.sum(Group.contributions.any(Contribution.amount))).filter(
            Group.id == group_id
        ).scalar()
        return result or 0.0

    def get_total_pledges(self, db: Session, *, group_id: int) -> float:
        """Get total pledges for a group"""
        result = db.query(func.sum(Group.contributions.any(Contribution.amount))).filter(
            Group.id == group_id,
            Contribution.type == "pledge"
        ).scalar()
        return result or 0.0

    def get_top_contributing_groups(self, db: Session, *, limit: int = 5) -> List[Group]:
        """Get top contributing groups by total contribution amount"""
        return (
            db.query(Group)
            .join(Contribution)
            .filter(Contribution.type == "contribution")
            .group_by(Group.id)
            .order_by(func.sum(Contribution.amount).desc())
            .limit(limit)
            .all()
        )

    def search(
        self,
        db: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Group]:
        """Search groups by name or description"""
        return (
            db.query(self.model)
            .filter(
                (Group.name.ilike(f"%{query}%")) |
                (Group.description.ilike(f"%{query}%"))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

group = CRUDGroup(Group) 