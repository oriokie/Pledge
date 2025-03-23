from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ....api import deps
from ....schemas import group as group_schemas
from ....models.group import Group
from ....models.member import Member
from ....models.user import User, UserRole

router = APIRouter()

@router.get("/", response_model=List[group_schemas.Group])
def read_groups(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve groups.
    """
    groups = db.query(Group).offset(skip).limit(limit).all()
    return groups

@router.post("/", response_model=group_schemas.Group)
def create_group(
    *,
    db: Session = Depends(deps.get_db),
    group_in: group_schemas.GroupCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Create new group.
    """
    group = db.query(Group).filter(Group.name == group_in.name).first()
    if group:
        raise HTTPException(
            status_code=400,
            detail="A group with this name already exists"
        )
    
    # Verify all member IDs exist
    if group_in.member_ids:
        members = db.query(Member).filter(
            Member.id.in_(group_in.member_ids)
        ).all()
        if len(members) != len(group_in.member_ids):
            raise HTTPException(
                status_code=400,
                detail="One or more member IDs are invalid"
            )
    
    group = Group(
        name=group_in.name,
        created_by_id=current_user.id
    )
    if group_in.member_ids:
        group.members = members
    
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

@router.get("/{group_id}", response_model=group_schemas.Group)
def read_group(
    *,
    db: Session = Depends(deps.get_db),
    group_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get group by ID.
    """
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )
    return group

@router.put("/{group_id}", response_model=group_schemas.Group)
def update_group(
    *,
    db: Session = Depends(deps.get_db),
    group_id: int,
    group_in: group_schemas.GroupUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Update a group.
    """
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )
    
    if group_in.name is not None:
        existing = db.query(Group).filter(
            Group.name == group_in.name,
            Group.id != group_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="A group with this name already exists"
            )
        group.name = group_in.name
    
    if group_in.member_ids is not None:
        members = db.query(Member).filter(
            Member.id.in_(group_in.member_ids)
        ).all()
        if len(members) != len(group_in.member_ids):
            raise HTTPException(
                status_code=400,
                detail="One or more member IDs are invalid"
            )
        group.members = members
    
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

@router.delete("/{group_id}", response_model=group_schemas.Group)
def delete_group(
    *,
    db: Session = Depends(deps.get_db),
    group_id: int,
    current_user: User = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Delete a group. Only admins can delete groups.
    """
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )
    
    db.delete(group)
    db.commit()
    return group

@router.get("/{group_id}/stats", response_model=group_schemas.GroupWithStats)
def get_group_stats(
    *,
    db: Session = Depends(deps.get_db),
    group_id: int,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get group statistics including member count and contribution totals.
    """
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(
            status_code=404,
            detail="Group not found"
        )
    
    return {
        "id": group.id,
        "name": group.name,
        "member_count": len(group.members),
        "total_contributions": sum(c.amount for c in group.contributions if c.contribution_date),
        "total_pledges": sum(c.amount for c in group.contributions)
    } 