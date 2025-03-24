from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ....api import deps
from ....schemas import pledge as pledge_schemas
from ....models.user import User
from ....services.pledge_service import PledgeService

router = APIRouter()

@router.get("/", response_model=List[pledge_schemas.Pledge])
def read_pledges(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    member_id: int = Query(None, description="Filter by member ID"),
    group_id: int = Query(None, description="Filter by group ID"),
    project_id: int = Query(None, description="Filter by project ID"),
    status: str = Query(None, description="Filter by pledge status"),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve pledges with optional filtering.
    """
    pledge_service = PledgeService(db)
    result = pledge_service.get_pledges(
        skip=skip,
        limit=limit,
        member_id=member_id,
        group_id=group_id,
        project_id=project_id,
        status=status
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result["pledges"]

@router.post("/", response_model=pledge_schemas.Pledge)
def create_pledge(
    *,
    db: Session = Depends(deps.get_db),
    pledge_in: pledge_schemas.PledgeCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Create new pledge.
    """
    pledge_service = PledgeService(db)
    result = pledge_service.create_pledge(pledge_in, current_user.id)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    
    # Get the created pledge
    pledge_result = pledge_service.get_pledge_by_id(result["pledge_id"])
    if pledge_result["status"] == "error":
        raise HTTPException(status_code=404, detail=pledge_result["message"])
    return pledge_result["pledge"]

@router.get("/{pledge_id}", response_model=pledge_schemas.Pledge)
def read_pledge(
    *,
    db: Session = Depends(deps.get_db),
    pledge_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get pledge by ID.
    """
    pledge_service = PledgeService(db)
    result = pledge_service.get_pledge_by_id(pledge_id)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result["pledge"]

@router.put("/{pledge_id}", response_model=pledge_schemas.Pledge)
def update_pledge(
    *,
    db: Session = Depends(deps.get_db),
    pledge_id: int,
    pledge_in: pledge_schemas.PledgeUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Update a pledge.
    """
    pledge_service = PledgeService(db)
    result = pledge_service.update_pledge(pledge_id, pledge_in)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    
    # Get the updated pledge
    pledge_result = pledge_service.get_pledge_by_id(pledge_id)
    if pledge_result["status"] == "error":
        raise HTTPException(status_code=404, detail=pledge_result["message"])
    return pledge_result["pledge"]

@router.delete("/{pledge_id}")
def delete_pledge(
    *,
    db: Session = Depends(deps.get_db),
    pledge_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Delete a pledge.
    """
    pledge_service = PledgeService(db)
    result = pledge_service.delete_pledge(pledge_id)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return {"status": "success", "message": "Pledge deleted successfully"} 