from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.audit import Audit
from app.schemas.audit import AuditCreate, AuditUpdate

class CRUDAudit(CRUDBase[Audit, AuditCreate, AuditUpdate]):
    def create(self, db: Session, *, obj_in: AuditCreate) -> Audit:
        db_obj = Audit(
            user_id=obj_in.user_id,
            action=obj_in.action,
            entity_type=obj_in.entity_type,
            entity_id=obj_in.entity_id,
            details=obj_in.details,
            ip_address=obj_in.ip_address,
            user_agent=obj_in.user_agent,
            created_at=datetime.utcnow(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Audit]:
        return (
            db.query(self.model)
            .filter(Audit.user_id == user_id)
            .order_by(Audit.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_entity(
        self,
        db: Session,
        *,
        entity_type: str,
        entity_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Audit]:
        return (
            db.query(self.model)
            .filter(
                Audit.entity_type == entity_type,
                Audit.entity_id == entity_id
            )
            .order_by(Audit.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        limit: int = 100
    ) -> List[Audit]:
        return (
            db.query(self.model)
            .filter(
                Audit.created_at >= start_date,
                Audit.created_at <= end_date
            )
            .order_by(Audit.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_action(
        self,
        db: Session,
        *,
        action: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Audit]:
        return (
            db.query(self.model)
            .filter(Audit.action == action)
            .order_by(Audit.created_at.desc())
            .offset(skip)
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
    ) -> List[Audit]:
        """Search audit logs by action, entity type, or details"""
        return (
            db.query(self.model)
            .filter(
                (Audit.action.ilike(f"%{query}%")) |
                (Audit.entity_type.ilike(f"%{query}%")) |
                (Audit.details.ilike(f"%{query}%"))
            )
            .order_by(Audit.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

audit = CRUDAudit(Audit) 