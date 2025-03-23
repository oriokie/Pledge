from typing import Generator
from sqlalchemy.orm import Session

from app import crud
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate

def test_create_member(db: Session) -> None:
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    assert member.name == "Test Member"
    assert member.phone_number == "1234567890"
    assert member.alias == "TM"
    assert member.is_active == True
    assert member.unique_code is not None
    assert len(member.unique_code) == 6

def test_get_member(db: Session) -> None:
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    stored_member = crud.member.get(db, id=member.id)
    assert stored_member
    assert member.id == stored_member.id
    assert member.name == stored_member.name
    assert member.phone_number == stored_member.phone_number
    assert member.alias == stored_member.alias
    assert member.is_active == stored_member.is_active
    assert member.unique_code == stored_member.unique_code

def test_get_member_by_phone(db: Session) -> None:
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    stored_member = crud.member.get_by_phone(db, phone_number="1234567890")
    assert stored_member
    assert member.id == stored_member.id
    assert member.name == stored_member.name
    assert member.phone_number == stored_member.phone_number
    assert member.alias == stored_member.alias
    assert member.is_active == stored_member.is_active
    assert member.unique_code == stored_member.unique_code

def test_get_member_by_code(db: Session) -> None:
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    stored_member = crud.member.get_by_code(db, unique_code=member.unique_code)
    assert stored_member
    assert member.id == stored_member.id
    assert member.name == stored_member.name
    assert member.phone_number == stored_member.phone_number
    assert member.alias == stored_member.alias
    assert member.is_active == stored_member.is_active
    assert member.unique_code == stored_member.unique_code

def test_get_multi(db: Session) -> None:
    member_in1 = MemberCreate(
        name="Test Member 1",
        phone_number="1234567890",
        alias="TM1",
        is_active=True,
    )
    member_in2 = MemberCreate(
        name="Test Member 2",
        phone_number="1234567891",
        alias="TM2",
        is_active=True,
    )
    member1 = crud.member.create(db, obj_in=member_in1)
    member2 = crud.member.create(db, obj_in=member_in2)
    stored_members = crud.member.get_multi(db)
    assert len(stored_members) >= 2
    assert any(m.id == member1.id for m in stored_members)
    assert any(m.id == member2.id for m in stored_members)

def test_update_member(db: Session) -> None:
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    member_in_update = MemberUpdate(
        name="Updated Member",
        alias="UM",
        is_active=False,
    )
    member2 = crud.member.update(db, db_obj=member, obj_in=member_in_update)
    assert member.id == member2.id
    assert member2.name == "Updated Member"
    assert member2.alias == "UM"
    assert member2.is_active == False
    assert member2.phone_number == member.phone_number
    assert member2.unique_code == member.unique_code

def test_search_member(db: Session) -> None:
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    stored_members = crud.member.search(db, search_term="Test")
    assert len(stored_members) > 0
    assert any(m.id == member.id for m in stored_members)

def test_search_member_by_phone(db: Session) -> None:
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    stored_members = crud.member.search(db, search_term="123456")
    assert len(stored_members) > 0
    assert any(m.id == member.id for m in stored_members)

def test_search_member_by_alias(db: Session) -> None:
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    stored_members = crud.member.search(db, search_term="TM")
    assert len(stored_members) > 0
    assert any(m.id == member.id for m in stored_members)

def test_search_member_no_results(db: Session) -> None:
    stored_members = crud.member.search(db, search_term="Nonexistent")
    assert len(stored_members) == 0 