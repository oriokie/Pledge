from typing import Generator
from sqlalchemy.orm import Session

from app import crud
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

def test_create_user(db: Session) -> None:
    phone_number = "test@example.com"
    password = "testpassword123"
    user_in = UserCreate(
        phone_number=phone_number,
        password=password,
        full_name="Test User",
        is_active=True,
        is_admin=False,
    )
    user = crud.user.create(db, obj_in=user_in)
    assert user.phone_number == phone_number
    assert user.full_name == "Test User"
    assert user.is_active == True
    assert user.is_admin == False
    assert user.hashed_password != password

def test_authenticate_user(db: Session) -> None:
    phone_number = "test@example.com"
    password = "testpassword123"
    user_in = UserCreate(
        phone_number=phone_number,
        password=password,
        full_name="Test User",
        is_active=True,
        is_admin=False,
    )
    user = crud.user.create(db, obj_in=user_in)
    authenticated_user = crud.user.authenticate(
        db, phone_number=phone_number, password=password
    )
    assert authenticated_user
    assert user.id == authenticated_user.id

def test_authenticate_user_incorrect_password(db: Session) -> None:
    phone_number = "test@example.com"
    password = "testpassword123"
    user_in = UserCreate(
        phone_number=phone_number,
        password=password,
        full_name="Test User",
        is_active=True,
        is_admin=False,
    )
    user = crud.user.create(db, obj_in=user_in)
    authenticated_user = crud.user.authenticate(
        db, phone_number=phone_number, password="wrongpassword"
    )
    assert not authenticated_user

def test_authenticate_user_inactive(db: Session) -> None:
    phone_number = "test@example.com"
    password = "testpassword123"
    user_in = UserCreate(
        phone_number=phone_number,
        password=password,
        full_name="Test User",
        is_active=False,
        is_admin=False,
    )
    user = crud.user.create(db, obj_in=user_in)
    authenticated_user = crud.user.authenticate(
        db, phone_number=phone_number, password=password
    )
    assert not authenticated_user

def test_get_by_phone(db: Session) -> None:
    phone_number = "test@example.com"
    password = "testpassword123"
    user_in = UserCreate(
        phone_number=phone_number,
        password=password,
        full_name="Test User",
        is_active=True,
        is_admin=False,
    )
    user = crud.user.create(db, obj_in=user_in)
    user_2 = crud.user.get_by_phone(db, phone_number=phone_number)
    assert user_2
    assert user.id == user_2.id
    assert user.phone_number == user_2.phone_number

def test_get_by_phone_not_found(db: Session) -> None:
    user = crud.user.get_by_phone(db, phone_number="nonexistent@example.com")
    assert not user

def test_is_active(db: Session) -> None:
    phone_number = "test@example.com"
    password = "testpassword123"
    user_in = UserCreate(
        phone_number=phone_number,
        password=password,
        full_name="Test User",
        is_active=True,
        is_admin=False,
    )
    user = crud.user.create(db, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active == True

def test_is_active_inactive(db: Session) -> None:
    phone_number = "test@example.com"
    password = "testpassword123"
    user_in = UserCreate(
        phone_number=phone_number,
        password=password,
        full_name="Test User",
        is_active=False,
        is_admin=False,
    )
    user = crud.user.create(db, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active == False

def test_is_admin(db: Session) -> None:
    phone_number = "test@example.com"
    password = "testpassword123"
    user_in = UserCreate(
        phone_number=phone_number,
        password=password,
        full_name="Test User",
        is_active=True,
        is_admin=True,
    )
    user = crud.user.create(db, obj_in=user_in)
    is_admin = crud.user.is_admin(user)
    assert is_admin == True

def test_is_admin_not_admin(db: Session) -> None:
    phone_number = "test@example.com"
    password = "testpassword123"
    user_in = UserCreate(
        phone_number=phone_number,
        password=password,
        full_name="Test User",
        is_active=True,
        is_admin=False,
    )
    user = crud.user.create(db, obj_in=user_in)
    is_admin = crud.user.is_admin(user)
    assert is_admin == False

def test_update_user(db: Session) -> None:
    phone_number = "test@example.com"
    password = "testpassword123"
    user_in = UserCreate(
        phone_number=phone_number,
        password=password,
        full_name="Test User",
        is_active=True,
        is_admin=False,
    )
    user = crud.user.create(db, obj_in=user_in)
    new_full_name = "Updated User"
    user_in_update = UserUpdate(full_name=new_full_name)
    user2 = crud.user.update(db, db_obj=user, obj_in=user_in_update)
    assert user.id == user2.id
    assert user2.full_name == new_full_name
    assert user2.phone_number == phone_number

def test_update_user_password(db: Session) -> None:
    phone_number = "test@example.com"
    password = "testpassword123"
    user_in = UserCreate(
        phone_number=phone_number,
        password=password,
        full_name="Test User",
        is_active=True,
        is_admin=False,
    )
    user = crud.user.create(db, obj_in=user_in)
    new_password = "newpassword123"
    user_in_update = UserUpdate(password=new_password)
    user2 = crud.user.update(db, db_obj=user, obj_in=user_in_update)
    assert user.id == user2.id
    assert user2.hashed_password != new_password
    assert user2.hashed_password != user.hashed_password 