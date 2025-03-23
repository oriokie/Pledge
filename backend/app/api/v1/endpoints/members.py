from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.utils.code_generator import generate_unique_code

router = APIRouter()

@router.get("/", response_model=List[schemas.Member])
def read_members(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(deps.get_current_user),
    search: str = Query(None, description="Search by name, alias, or phone number"),
) -> Any:
    """
    Retrieve members.
    """
    if search:
        members = crud.member.search(db, search_term=search, skip=skip, limit=limit)
    else:
        members = crud.member.get_multi(db, skip=skip, limit=limit)
    return members

@router.post("/", response_model=schemas.Member)
def create_member(
    *,
    db: Session = Depends(deps.get_db),
    member_in: schemas.MemberCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new member.
    """
    member = crud.member.get_by_phone(db, phone_number=member_in.phone_number)
    if member:
        raise HTTPException(
            status_code=400,
            detail="The member with this phone number already exists in the system.",
        )
    
    # Generate unique code
    unique_code = generate_unique_code(db)
    
    # Create member with unique code and current user as creator/updater
    member_in_dict = member_in.dict()
    member_in_dict["unique_code"] = unique_code
    member_in_dict["created_by"] = current_user.id
    member_in_dict["updated_by"] = current_user.id
    
    member = crud.member.create(db, obj_in=member_in_dict)
    return member

@router.get("/{member_id}", response_model=schemas.Member)
def read_member(
    *,
    db: Session = Depends(deps.get_db),
    member_id: int,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get member by ID.
    """
    member = crud.member.get(db, id=member_id)
    if not member:
        raise HTTPException(
            status_code=404,
            detail="The member with this id does not exist in the system",
        )
    return member

@router.put("/{member_id}", response_model=schemas.Member)
def update_member(
    *,
    db: Session = Depends(deps.get_db),
    member_id: int,
    member_in: schemas.MemberUpdate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a member.
    """
    member = crud.member.get(db, id=member_id)
    if not member:
        raise HTTPException(
            status_code=404,
            detail="The member with this id does not exist in the system",
        )
    
    # Update member with current user as updater
    member_in_dict = member_in.dict(exclude_unset=True)
    member_in_dict["updated_by"] = current_user.id
    
    member = crud.member.update(db, db_obj=member, obj_in=member_in_dict)
    return member

@router.delete("/{member_id}", response_model=schemas.Member)
def delete_member(
    *,
    db: Session = Depends(deps.get_db),
    member_id: int,
    current_user: schemas.User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Delete a member.
    """
    member = crud.member.get(db, id=member_id)
    if not member:
        raise HTTPException(
            status_code=404,
            detail="The member with this id does not exist in the system",
        )
    member = crud.member.remove(db, id=member_id)
    return member

@router.get("/code/{unique_code}", response_model=schemas.Member)
def read_member_by_code(
    *,
    db: Session = Depends(deps.get_db),
    unique_code: str,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get member by unique code.
    """
    member = crud.member.get_by_code(db, unique_code=unique_code)
    if not member:
        raise HTTPException(
            status_code=404,
            detail="The member with this code does not exist in the system",
        )
    return member 