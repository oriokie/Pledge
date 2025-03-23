from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app import crud, schemas
from app.api import deps
from app.utils.report_generator import (
    generate_project_report,
    generate_group_report,
    generate_member_report,
    save_report_to_excel
)

router = APIRouter()

@router.get("/projects/{project_id}")
def get_project_report(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    download: bool = False,
) -> Any:
    """
    Generate a report for a specific project.
    """
    project = crud.project.get(db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail="The project with this id does not exist in the system",
        )
    
    df = generate_project_report(db, project_id, start_date, end_date)
    
    if download:
        filename = f"project_report_{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = save_report_to_excel(df, filename)
        if not filepath:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate Excel report",
            )
        return FileResponse(
            filepath,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=filename
        )
    
    return df.to_dict(orient="records")

@router.get("/groups/{group_id}")
def get_group_report(
    *,
    db: Session = Depends(deps.get_db),
    group_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    download: bool = False,
) -> Any:
    """
    Generate a report for a specific group.
    """
    group = crud.group.get(db, id=group_id)
    if not group:
        raise HTTPException(
            status_code=404,
            detail="The group with this id does not exist in the system",
        )
    
    df = generate_group_report(db, group_id, start_date, end_date)
    
    if download:
        filename = f"group_report_{group_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = save_report_to_excel(df, filename)
        if not filepath:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate Excel report",
            )
        return FileResponse(
            filepath,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=filename
        )
    
    return df.to_dict(orient="records")

@router.get("/members/{member_id}")
def get_member_report(
    *,
    db: Session = Depends(deps.get_db),
    member_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    download: bool = False,
) -> Any:
    """
    Generate a report for a specific member.
    """
    member = crud.member.get(db, id=member_id)
    if not member:
        raise HTTPException(
            status_code=404,
            detail="The member with this id does not exist in the system",
        )
    
    df = generate_member_report(db, member_id, start_date, end_date)
    
    if download:
        filename = f"member_report_{member_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = save_report_to_excel(df, filename)
        if not filepath:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate Excel report",
            )
        return FileResponse(
            filepath,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=filename
        )
    
    return df.to_dict(orient="records")

@router.get("/dashboard")
def get_dashboard_data(
    *,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get dashboard data including total pledges, contributions, and top groups.
    """
    # Get total pledges and contributions
    total_pledged = crud.contribution.get_total_pledged(db)
    total_contributed = crud.contribution.get_total_contributed(db)
    
    # Get top contributing groups
    top_groups = crud.group.get_top_contributing_groups(db, limit=5)
    
    # Get active projects
    active_projects = crud.project.get_active_projects(db)
    
    return {
        "total_pledged": total_pledged,
        "total_contributed": total_contributed,
        "remaining_balance": total_pledged - total_contributed,
        "top_groups": top_groups,
        "active_projects": active_projects,
    } 