from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Project]:
        return db.query(Project).filter(Project.name == name).first()

    def create(self, db: Session, *, obj_in: ProjectCreate) -> Project:
        db_obj = Project(
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
        self, db: Session, *, db_obj: Project, obj_in: Union[ProjectUpdate, Dict[str, Any]]
    ) -> Project:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_total_contributions(self, db: Session, *, project_id: int) -> float:
        """Get total contributions for a project"""
        result = db.query(func.sum(Project.contributions.any(Contribution.amount))).filter(
            Project.id == project_id,
            Contribution.type == "contribution"
        ).scalar()
        return result or 0.0

    def get_total_pledges(self, db: Session, *, project_id: int) -> float:
        """Get total pledges for a project"""
        result = db.query(func.sum(Project.contributions.any(Contribution.amount))).filter(
            Project.id == project_id,
            Contribution.type == "pledge"
        ).scalar()
        return result or 0.0

    def get_active_projects(self, db: Session) -> List[Project]:
        """Get all active projects"""
        return (
            db.query(self.model)
            .filter(Project.status == "active")
            .order_by(Project.created_at.desc())
            .all()
        )

    def get_completed_projects(self, db: Session) -> List[Project]:
        """Get all completed projects"""
        return (
            db.query(self.model)
            .filter(Project.status == "completed")
            .order_by(Project.created_at.desc())
            .all()
        )

    def search(
        self,
        db: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """Search projects by name or description"""
        return (
            db.query(self.model)
            .filter(
                (Project.name.ilike(f"%{query}%")) |
                (Project.description.ilike(f"%{query}%"))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

project = CRUDProject(Project) 