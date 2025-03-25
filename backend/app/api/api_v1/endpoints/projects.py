from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ....api import deps
from ....schemas import project as project_schemas
from ....models.project import Project
from ....models.contribution import Contribution
from ....models.user import User, UserRole
from decimal import Decimal

router = APIRouter()

@router.get("/", response_model=List[project_schemas.Project])
def read_projects(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve projects.
    """
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects

@router.post("/", response_model=project_schemas.Project)
def create_project(
    *,
    db: Session = Depends(deps.get_db),
    project_in: project_schemas.ProjectCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Create new project.
    """
    project = db.query(Project).filter(Project.name == project_in.name).first()
    if project:
        raise HTTPException(
            status_code=400,
            detail="A project with this name already exists"
        )
    
    project_data = project_in.dict()
    project = Project(
        **project_data,
        created_by_id=current_user.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/{project_id}", response_model=project_schemas.Project)
def read_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get project by ID.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    return project

@router.put("/{project_id}", response_model=project_schemas.Project)
def update_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    project_in: project_schemas.ProjectUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Update a project.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    
    if project_in.name is not None:
        existing = db.query(Project).filter(
            Project.name == project_in.name,
            Project.id != project_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="A project with this name already exists"
            )
    
    update_data = project_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}", response_model=project_schemas.Project)
def delete_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    current_user: User = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Delete a project. Only admins can delete projects.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()
    return project

@router.get("/{project_id}/stats", response_model=project_schemas.ProjectStats)
def get_project_stats(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get project statistics including contribution totals and completion percentage.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    
    # Get contribution statistics
    contributions = db.query(
        func.sum(Contribution.amount).label("total_contributions"),
        func.count(Contribution.id).label("contribution_count")
    ).filter(
        Contribution.project_id == project_id,
        Contribution.contribution_date.isnot(None)
    ).first()

    # Get pledge total
    pledges = db.query(
        func.sum(Contribution.amount).label("total_pledges")
    ).filter(
        Contribution.project_id == project_id
    ).scalar() or Decimal(0)

    total_contributions = contributions[0] or Decimal(0)
    contribution_count = contributions[1] or 0
    completion_percentage = (total_contributions / pledges * 100) if pledges > 0 else Decimal(0)

    return {
        "id": project.id,
        "name": project.name,
        "total_contributions": total_contributions,
        "total_pledges": pledges,
        "contribution_count": contribution_count,
        "completion_percentage": completion_percentage
    } 