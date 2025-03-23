from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ....api import deps
from ....schemas import member as member_schemas
from ....models.member import Member
from ....models.user import User, UserRole
import random
import string

router = APIRouter()

def generate_unique_code(db: Session) -> str:
    """Generate a unique 6-digit code for a member"""
    while True:
        code = ''.join(random.choices(string.digits, k=6))
        exists = db.query(Member).filter(Member.unique_code == code).first()
        if not exists:
            return code

@router.get("/", response_model=List[member_schemas.Member])
def read_members(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve members.
    """
    members = db.query(Member).offset(skip).limit(limit).all()
    return members

@router.post("/", response_model=member_schemas.Member)
def create_member(
    *,
    db: Session = Depends(deps.get_db),
    member_in: member_schemas.MemberCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Create new member.
    """
    member = db.query(Member).filter(
        Member.phone_number == member_in.phone_number
    ).first()
    if member:
        raise HTTPException(
            status_code=400,
            detail="A member with this phone number already exists"
        )
    
    member = Member(
        **member_in.dict(),
        created_by_id=current_user.id,
        unique_code=generate_unique_code(db)
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

@router.get("/search", response_model=List[member_schemas.MemberSearchResult])
def search_members(
    *,
    db: Session = Depends(deps.get_db),
    query: str = Query(..., min_length=1),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Search members by name, alias, phone number, or unique code.
    """
    members = db.query(Member).filter(
        or_(
            Member.name.ilike(f"%{query}%"),
            Member.alias1.ilike(f"%{query}%"),
            Member.alias2.ilike(f"%{query}%"),
            Member.phone_number.ilike(f"%{query}%"),
            Member.unique_code == query
        )
    ).all()

    results = []
    for member in members:
        matched_field = "name"
        if query.lower() in member.alias1.lower():
            matched_field = "alias1"
        elif query.lower() in member.alias2.lower():
            matched_field = "alias2"
        elif query in member.phone_number:
            matched_field = "phone"
        elif query == member.unique_code:
            matched_field = "unique_code"
        
        results.append(member_schemas.MemberSearchResult(
            id=member.id,
            name=member.name,
            unique_code=member.unique_code,
            matched_field=matched_field
        ))
    
    return results

@router.put("/{member_id}", response_model=member_schemas.Member)
def update_member(
    *,
    db: Session = Depends(deps.get_db),
    member_id: int,
    member_in: member_schemas.MemberUpdate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Update a member.
    """
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )
    
    update_data = member_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(member, field, value)
    
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

@router.delete("/{member_id}", response_model=member_schemas.Member)
def delete_member(
    *,
    db: Session = Depends(deps.get_db),
    member_id: int,
    current_user: User = Depends(deps.get_current_active_admin)
) -> Any:
    """
    Delete a member. Only admins can delete members.
    """
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )
    
    db.delete(member)
    db.commit()
    return member 