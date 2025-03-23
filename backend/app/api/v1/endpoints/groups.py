from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Group])
def read_groups(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve groups.
    """
    groups = crud.group.get_multi(db, skip=skip, limit=limit)
    return groups

@router.post("/", response_model=schemas.Group)
def create_group(
    *,
    db: Session = Depends(deps.get_db),
    group_in: schemas.GroupCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new group.
    """
    group = crud.group.get_by_name(db, name=group_in.name)
    if group:
        raise HTTPException(
            status_code=400,
            detail="The group with this name already exists in the system.",
        )
    
    # Create group with current user as creator/updater
    group_in_dict = group_in.dict()
    group_in_dict["created_by"] = current_user.id
    group_in_dict["updated_by"] = current_user.id
    
    group = crud.group.create(db, obj_in=group_in_dict)
    
    # Add members if specified
    if group_in.member_ids:
        for member_id in group_in.member_ids:
            member = crud.member.get(db, id=member_id)
            if member:
                group.members.append(member)
        db.commit()
    
    return group

@router.get("/{group_id}", response_model=schemas.Group)
def read_group(
    *,
    db: Session = Depends(deps.get_db),
    group_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get group by ID.
    """
    group = crud.group.get(db, id=group_id)
    if not group:
        raise HTTPException(
            status_code=404,
            detail="The group with this id does not exist in the system",
        )
    return group

@router.put("/{group_id}", response_model=schemas.Group)
def update_group(
    *,
    db: Session = Depends(deps.get_db),
    group_id: int,
    group_in: schemas.GroupUpdate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a group.
    """
    group = crud.group.get(db, id=group_id)
    if not group:
        raise HTTPException(
            status_code=404,
            detail="The group with this id does not exist in the system",
        )
    
    # Update group with current user as updater
    group_in_dict = group_in.dict(exclude_unset=True)
    group_in_dict["updated_by"] = current_user.id
    
    group = crud.group.update(db, db_obj=group, obj_in=group_in_dict)
    
    # Update members if specified
    if group_in.member_ids is not None:
        group.members = []
        for member_id in group_in.member_ids:
            member = crud.member.get(db, id=member_id)
            if member:
                group.members.append(member)
        db.commit()
    
    return group

@router.delete("/{group_id}", response_model=schemas.Group)
def delete_group(
    *,
    db: Session = Depends(deps.get_db),
    group_id: int,
    current_user: schemas.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Delete a group.
    """
    group = crud.group.get(db, id=group_id)
    if not group:
        raise HTTPException(
            status_code=404,
            detail="The group with this id does not exist in the system",
        )
    group = crud.group.remove(db, id=group_id)
    return group

@router.post("/{group_id}/members/{member_id}", response_model=schemas.Group)
def add_member_to_group(
    *,
    db: Session = Depends(deps.get_db),
    group_id: int,
    member_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Add a member to a group.
    """
    group = crud.group.get(db, id=group_id)
    if not group:
        raise HTTPException(
            status_code=404,
            detail="The group with this id does not exist in the system",
        )
    
    member = crud.member.get(db, id=member_id)
    if not member:
        raise HTTPException(
            status_code=404,
            detail="The member with this id does not exist in the system",
        )
    
    if member in group.members:
        raise HTTPException(
            status_code=400,
            detail="The member is already in this group",
        )
    
    group.members.append(member)
    db.commit()
    return group

@router.delete("/{group_id}/members/{member_id}", response_model=schemas.Group)
def remove_member_from_group(
    *,
    db: Session = Depends(deps.get_db),
    group_id: int,
    member_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Remove a member from a group.
    """
    group = crud.group.get(db, id=group_id)
    if not group:
        raise HTTPException(
            status_code=404,
            detail="The group with this id does not exist in the system",
        )
    
    member = crud.member.get(db, id=member_id)
    if not member:
        raise HTTPException(
            status_code=404,
            detail="The member with this id does not exist in the system",
        )
    
    if member not in group.members:
        raise HTTPException(
            status_code=400,
            detail="The member is not in this group",
        )
    
    group.members.remove(member)
    db.commit()
    return group 