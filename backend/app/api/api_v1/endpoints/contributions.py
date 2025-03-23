from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from ....api import deps
from ....schemas import contribution as contribution_schemas
from ....models.contribution import Contribution
from ....models.member import Member
from ....models.group import Group
from ....models.project import Project
from ....models.user import User, UserRole
from ....core.celery_app import celery_app

router = APIRouter()

@router.get("/", response_model=List[contribution_schemas.Contribution])
def read_contributions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    member_id: Optional[int] = None,
    group_id: Optional[int] = None,
    project_id: Optional[int] = None,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve contributions with optional filtering.
    """
    query = db.query(Contribution)
    
    if member_id:
        query = query.filter(Contribution.member_id == member_id)
    if group_id:
        query = query.filter(Contribution.group_id == group_id)
    if project_id:
        query = query.filter(Contribution.project_id == project_id)
    
    contributions = query.offset(skip).limit(limit).all()
    return contributions

@router.post("/", response_model=contribution_schemas.Contribution)
def create_contribution(
    *,
    db: Session = Depends(deps.get_db),
    contribution_in: contribution_schemas.ContributionCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Create new contribution or pledge.
    """
    # Verify member exists
    member = db.query(Member).filter(Member.id == contribution_in.member_id).first()
    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )
    
    # Verify project exists
    project = db.query(Project).filter(Project.id == contribution_in.project_id).first()
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    
    # Verify group exists if provided
    if contribution_in.group_id:
        group = db.query(Group).filter(Group.id == contribution_in.group_id).first()
        if not group:
            raise HTTPException(
                status_code=404,
                detail="Group not found"
            )
        # Verify member belongs to group
        if member not in group.members:
            raise HTTPException(
                status_code=400,
                detail="Member does not belong to the specified group"
            )
    
    contribution = Contribution(
        **contribution_in.dict(),
        created_by_id=current_user.id
    )
    db.add(contribution)
    db.commit()
    db.refresh(contribution)

    # Send SMS notification if contribution is made (not just pledged)
    if contribution.contribution_date:
        celery_app.send_task(
            "app.tasks.send_contribution_confirmation",
            args=[contribution.id]
        )
    
    return contribution

@router.get("/{contribution_id}", response_model=contribution_schemas.Contribution)
def read_contribution(
    *,
    db: Session = Depends(deps.get_db),
    contribution_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get contribution by ID.
    """
    contribution = db.query(Contribution).filter(Contribution.id == contribution_id).first()
    if not contribution:
        raise HTTPException(
            status_code=404,
            detail="Contribution not found"
        )
    return contribution

@router.put("/{contribution_id}", response_model=contribution_schemas.Contribution)
def update_contribution(
    *,
    db: Session = Depends(deps.get_db),
    contribution_id: int,
    contribution_in: contribution_schemas.ContributionUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Update a contribution.
    """
    contribution = db.query(Contribution).filter(Contribution.id == contribution_id).first()
    if not contribution:
        raise HTTPException(
            status_code=404,
            detail="Contribution not found"
        )
    
    update_data = contribution_in.dict(exclude_unset=True)
    
    # If marking as contributed, send SMS notification
    if (
        "contribution_date" in update_data 
        and update_data["contribution_date"] 
        and not contribution.contribution_date
    ):
        celery_app.send_task(
            "app.tasks.send_contribution_confirmation",
            args=[contribution.id]
        )
    
    for field, value in update_data.items():
        setattr(contribution, field, value)
    
    db.add(contribution)
    db.commit()
    db.refresh(contribution)
    return contribution

@router.delete("/{contribution_id}", response_model=contribution_schemas.Contribution)
def delete_contribution(
    *,
    db: Session = Depends(deps.get_db),
    contribution_id: int,
    current_user: User = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Delete a contribution. Only admins can delete contributions.
    """
    contribution = db.query(Contribution).filter(Contribution.id == contribution_id).first()
    if not contribution:
        raise HTTPException(
            status_code=404,
            detail="Contribution not found"
        )
    
    db.delete(contribution)
    db.commit()
    return contribution

@router.get("/summary", response_model=contribution_schemas.ContributionSummary)
def get_contribution_summary(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int = Query(..., description="Project ID to summarize contributions for"),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get contribution summary for a project within an optional date range.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )
    
    query = db.query(
        func.sum(Contribution.amount).label("total_amount"),
        func.count(Contribution.id).label("contribution_count"),
        func.count(func.distinct(Contribution.member_id)).label("member_count"),
        func.count(func.distinct(Contribution.group_id)).label("group_count")
    ).filter(Contribution.project_id == project_id)
    
    if start_date:
        query = query.filter(Contribution.contribution_date >= start_date)
    if end_date:
        query = query.filter(Contribution.contribution_date <= end_date)
    
    result = query.first()
    
    return {
        "total_amount": result[0] or 0,
        "contribution_count": result[1],
        "member_count": result[2],
        "group_count": result[3],
        "project_name": project.name,
        "start_date": start_date or project.start_date,
        "end_date": end_date or project.end_date
    } 