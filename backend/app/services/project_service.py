from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.project import Project
from ..models.group import Group
from ..core.utils import format_currency
from ..schemas.project import ProjectCreate, ProjectUpdate

class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    def create_project(
        self,
        project_data: ProjectCreate
    ) -> Dict[str, Any]:
        """Create a new project."""
        try:
            # Check if project name already exists
            if self.db.query(Project).filter(Project.name == project_data.name).first():
                return {"status": "error", "message": "Project name already exists"}

            # Create project
            project = Project(
                name=project_data.name,
                description=project_data.description,
                target_amount=project_data.target_amount,
                start_date=project_data.start_date,
                end_date=project_data.end_date,
                status=project_data.status,
                is_active=project_data.is_active
            )
            self.db.add(project)
            self.db.commit()

            return {
                "status": "success",
                "project_id": project.id,
                "message": "Project created successfully"
            }
        except IntegrityError:
            return {"status": "error", "message": "Project already exists"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_project_by_id(
        self,
        project_id: int
    ) -> Dict[str, Any]:
        """Get project by ID."""
        try:
            project = self.db.query(Project).filter(Project.id == project_id).first()
            if not project:
                return {"status": "error", "message": "Project not found"}

            # Calculate total contributions from all groups
            total_contributions = sum(
                sum(c.amount for c in g.contributions if c.status == "completed")
                for g in project.groups
            )
            progress_percentage = (total_contributions / project.target_amount * 100) if project.target_amount > 0 else 0

            return {
                "status": "success",
                "project": {
                    "id": project.id,
                    "name": project.name,
                    "description": project.description,
                    "target_amount": format_currency(project.target_amount),
                    "total_contributions": format_currency(total_contributions),
                    "progress_percentage": progress_percentage,
                    "start_date": project.start_date.isoformat() if project.start_date else None,
                    "end_date": project.end_date.isoformat() if project.end_date else None,
                    "status": project.status,
                    "is_active": project.is_active,
                    "group_count": len(project.groups),
                    "created_at": project.created_at.isoformat(),
                    "updated_at": project.updated_at.isoformat()
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def update_project(
        self,
        project_id: int,
        project_data: ProjectUpdate
    ) -> Dict[str, Any]:
        """Update project information."""
        try:
            project = self.db.query(Project).filter(Project.id == project_id).first()
            if not project:
                return {"status": "error", "message": "Project not found"}

            # Update fields if provided
            if project_data.name and project_data.name != project.name:
                if self.db.query(Project).filter(
                    Project.name == project_data.name,
                    Project.id != project_id
                ).first():
                    return {"status": "error", "message": "Project name already exists"}
                project.name = project_data.name

            if project_data.description:
                project.description = project_data.description

            if project_data.target_amount:
                project.target_amount = project_data.target_amount

            if project_data.start_date:
                project.start_date = project_data.start_date

            if project_data.end_date:
                project.end_date = project_data.end_date

            if project_data.status:
                project.status = project_data.status

            if project_data.is_active is not None:
                project.is_active = project_data.is_active

            self.db.commit()

            return {
                "status": "success",
                "message": "Project updated successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_project(
        self,
        project_id: int
    ) -> Dict[str, Any]:
        """Delete a project."""
        try:
            project = self.db.query(Project).filter(Project.id == project_id).first()
            if not project:
                return {"status": "error", "message": "Project not found"}

            # Check if project has groups
            if project.groups:
                return {"status": "error", "message": "Cannot delete project with groups"}

            self.db.delete(project)
            self.db.commit()

            return {
                "status": "success",
                "message": "Project deleted successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_projects(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Get list of projects with optional filters."""
        try:
            query = self.db.query(Project)

            if status:
                query = query.filter(Project.status == status)
            if is_active is not None:
                query = query.filter(Project.is_active == is_active)

            total_count = query.count()
            projects = query.offset(skip).limit(limit).all()

            return {
                "status": "success",
                "total_count": total_count,
                "projects": [
                    {
                        "id": project.id,
                        "name": project.name,
                        "description": project.description,
                        "target_amount": format_currency(project.target_amount),
                        "total_contributions": format_currency(
                            sum(
                                sum(c.amount for c in g.contributions if c.status == "completed")
                                for g in project.groups
                            )
                        ),
                        "start_date": project.start_date.isoformat() if project.start_date else None,
                        "end_date": project.end_date.isoformat() if project.end_date else None,
                        "status": project.status,
                        "is_active": project.is_active,
                        "group_count": len(project.groups),
                        "created_at": project.created_at.isoformat(),
                        "updated_at": project.updated_at.isoformat()
                    }
                    for project in projects
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_project_groups(
        self,
        project_id: int,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Get list of groups in a project."""
        try:
            project = self.db.query(Project).filter(Project.id == project_id).first()
            if not project:
                return {"status": "error", "message": "Project not found"}

            query = project.groups

            if is_active is not None:
                query = query.filter(Group.is_active == is_active)

            total_count = len(query)
            groups = query[skip:skip + limit]

            return {
                "status": "success",
                "total_count": total_count,
                "groups": [
                    {
                        "id": group.id,
                        "name": group.name,
                        "description": group.description,
                        "target_amount": format_currency(group.target_amount),
                        "total_contributions": format_currency(
                            sum(c.amount for c in group.contributions if c.status == "completed")
                        ),
                        "start_date": group.start_date.isoformat() if group.start_date else None,
                        "end_date": group.end_date.isoformat() if group.end_date else None,
                        "is_active": group.is_active,
                        "member_count": len(group.members),
                        "created_at": group.created_at.isoformat(),
                        "updated_at": group.updated_at.isoformat()
                    }
                    for group in groups
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)} 