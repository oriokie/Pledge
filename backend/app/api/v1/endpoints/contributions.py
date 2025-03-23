from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.services.sms import sms_service

router = APIRouter()

@router.get("/", response_model=List[schemas.Contribution])
def read_contributions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(deps.get_current_user),
    project_id: int = Query(None, description="Filter by project ID"),
    member_id: int = Query(None, description="Filter by member ID"),
    group_id: int = Query(None, description="Filter by group ID"),
    search: str = Query(None, description="Search by member name, alias, or phone number"),
) -> Any:
    """
    Retrieve contributions.
    """
    if search:
        contributions = crud.contribution.search(
            db,
            search_term=search,
            project_id=project_id,
            member_id=member_id,
            group_id=group_id,
            skip=skip,
            limit=limit
        )
    else:
        contributions = crud.contribution.get_multi(
            db,
            project_id=project_id,
            member_id=member_id,
            group_id=group_id,
            skip=skip,
            limit=limit
        )
    return contributions

@router.post("/", response_model=schemas.Contribution)
def create_contribution(
    *,
    db: Session = Depends(deps.get_db),
    contribution_in: schemas.ContributionCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new contribution or pledge.
    """
    # Verify member exists
    member = crud.member.get(db, id=contribution_in.member_id)
    if not member:
        raise HTTPException(
            status_code=404,
            detail="The member with this id does not exist in the system",
        )
    
    # Verify project exists
    project = crud.project.get(db, id=contribution_in.project_id)
    if not project:
        raise HTTPException(
            status_code=404,
            detail="The project with this id does not exist in the system",
        )
    
    # Verify group exists if specified
    if contribution_in.group_id:
        group = crud.group.get(db, id=contribution_in.group_id)
        if not group:
            raise HTTPException(
                status_code=404,
                detail="The group with this id does not exist in the system",
            )
        if member not in group.members:
            raise HTTPException(
                status_code=400,
                detail="The member is not in this group",
            )
    
    # Create contribution with current user as creator/updater
    contribution_in_dict = contribution_in.dict()
    contribution_in_dict["created_by"] = current_user.id
    contribution_in_dict["updated_by"] = current_user.id
    
    contribution = crud.contribution.create(db, obj_in=contribution_in_dict)
    
    # Send SMS notification
    if contribution.type == "pledge":
        sms_service.send_pledge_confirmation(
            member.phone_number,
            contribution.amount,
            project.name
        )
    else:
        sms_service.send_contribution_confirmation(
            member.phone_number,
            contribution.amount,
            project.name
        )
    
    return contribution

@router.get("/{contribution_id}", response_model=schemas.Contribution)
def read_contribution(
    *,
    db: Session = Depends(deps.get_db),
    contribution_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get contribution by ID.
    """
    contribution = crud.contribution.get(db, id=contribution_id)
    if not contribution:
        raise HTTPException(
            status_code=404,
            detail="The contribution with this id does not exist in the system",
        )
    return contribution

@router.put("/{contribution_id}", response_model=schemas.Contribution)
def update_contribution(
    *,
    db: Session = Depends(deps.get_db),
    contribution_id: int,
    contribution_in: schemas.ContributionUpdate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a contribution.
    """
    contribution = crud.contribution.get(db, id=contribution_id)
    if not contribution:
        raise HTTPException(
            status_code=404,
            detail="The contribution with this id does not exist in the system",
        )
    
    # Update contribution with current user as updater
    contribution_in_dict = contribution_in.dict(exclude_unset=True)
    contribution_in_dict["updated_by"] = current_user.id
    
    contribution = crud.contribution.update(
        db,
        db_obj=contribution,
        obj_in=contribution_in_dict
    )
    return contribution

@router.delete("/{contribution_id}", response_model=schemas.Contribution)
def delete_contribution(
    *,
    db: Session = Depends(deps.get_db),
    contribution_id: int,
    current_user: schemas.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Delete a contribution.
    """
    contribution = crud.contribution.get(db, id=contribution_id)
    if not contribution:
        raise HTTPException(
            status_code=404,
            detail="The contribution with this id does not exist in the system",
        )
    contribution = crud.contribution.remove(db, id=contribution_id)
    return contribution

@router.post("/{contribution_id}/fulfill", response_model=schemas.Contribution)
def fulfill_pledge(
    *,
    db: Session = Depends(deps.get_db),
    contribution_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Convert a pledge to a contribution.
    """
    contribution = crud.contribution.get(db, id=contribution_id)
    if not contribution:
        raise HTTPException(
            status_code=404,
            detail="The contribution with this id does not exist in the system",
        )
    
    if contribution.type != "pledge":
        raise HTTPException(
            status_code=400,
            detail="This is not a pledge",
        )
    
    # Update contribution type and add contribution date
    contribution.type = "contribution"
    contribution.contribution_date = datetime.utcnow().date()
    contribution.updated_by = current_user.id
    db.commit()
    
    # Send SMS notification
    sms_service.send_contribution_confirmation(
        contribution.member.phone_number,
        contribution.amount,
        contribution.project.name
    )
    
    return contribution 