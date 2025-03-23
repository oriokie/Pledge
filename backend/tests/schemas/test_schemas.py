import pytest
from datetime import datetime, timedelta
from app.schemas.user import UserCreate, UserUpdate, UserRole
from app.schemas.member import MemberCreate, MemberUpdate
from app.schemas.group import GroupCreate, GroupUpdate
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.schemas.contribution import ContributionCreate, ContributionUpdate, PaymentMethod
from app.schemas.sms import SMSRequest, SMSResponse

def test_user_schemas():
    # Test UserCreate
    user_data = {
        "email": "test@example.com",
        "password": "test_password123",
        "full_name": "Test User",
        "role": UserRole.STAFF
    }
    user_create = UserCreate(**user_data)
    assert user_create.email == user_data["email"]
    assert user_create.full_name == user_data["full_name"]
    assert user_create.role == user_data["role"]
    
    # Test UserUpdate
    update_data = {
        "full_name": "Updated Name",
        "role": UserRole.ADMIN
    }
    user_update = UserUpdate(**update_data)
    assert user_update.full_name == update_data["full_name"]
    assert user_update.role == update_data["role"]
    
    # Test validation
    with pytest.raises(ValueError):
        UserCreate(email="invalid", password="test123", full_name="Test User")
    
    with pytest.raises(ValueError):
        UserCreate(email="test@example.com", password="short", full_name="Test User")

def test_member_schemas():
    # Test MemberCreate
    member_data = {
        "name": "Test Member",
        "alias": "TM",
        "phone_number": "+1234567890"
    }
    member_create = MemberCreate(**member_data)
    assert member_create.name == member_data["name"]
    assert member_create.alias == member_data["alias"]
    assert member_create.phone_number == member_data["phone_number"]
    
    # Test MemberUpdate
    update_data = {
        "name": "Updated Name",
        "alias": "UN"
    }
    member_update = MemberUpdate(**update_data)
    assert member_update.name == update_data["name"]
    assert member_update.alias == update_data["alias"]
    
    # Test validation
    with pytest.raises(ValueError):
        MemberCreate(name="Test", alias="T", phone_number="invalid")
    
    with pytest.raises(ValueError):
        MemberCreate(name="", alias="TM", phone_number="+1234567890")

def test_group_schemas():
    # Test GroupCreate
    group_data = {
        "name": "Test Group",
        "description": "Test group description",
        "member_ids": [1, 2, 3]
    }
    group_create = GroupCreate(**group_data)
    assert group_create.name == group_data["name"]
    assert group_create.description == group_data["description"]
    assert group_create.member_ids == group_data["member_ids"]
    
    # Test GroupUpdate
    update_data = {
        "name": "Updated Group",
        "member_ids": [4, 5, 6]
    }
    group_update = GroupUpdate(**update_data)
    assert group_update.name == update_data["name"]
    assert group_update.member_ids == update_data["member_ids"]
    
    # Test validation
    with pytest.raises(ValueError):
        GroupCreate(name="", description="Test", member_ids=[1])

def test_project_schemas():
    # Test ProjectCreate
    project_data = {
        "name": "Test Project",
        "description": "Test project description",
        "target_amount": 10000.0,
        "start_date": datetime.now(),
        "end_date": datetime.now() + timedelta(days=30)
    }
    project_create = ProjectCreate(**project_data)
    assert project_create.name == project_data["name"]
    assert project_create.description == project_data["description"]
    assert project_create.target_amount == project_data["target_amount"]
    assert project_create.start_date == project_data["start_date"]
    assert project_create.end_date == project_data["end_date"]
    
    # Test ProjectUpdate
    update_data = {
        "name": "Updated Project",
        "target_amount": 20000.0
    }
    project_update = ProjectUpdate(**update_data)
    assert project_update.name == update_data["name"]
    assert project_update.target_amount == update_data["target_amount"]
    
    # Test validation
    with pytest.raises(ValueError):
        ProjectCreate(
            name="Test",
            description="Test",
            target_amount=-1000.0,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30)
        )
    
    with pytest.raises(ValueError):
        ProjectCreate(
            name="Test",
            description="Test",
            target_amount=10000.0,
            start_date=datetime.now() + timedelta(days=30),
            end_date=datetime.now()
        )

def test_contribution_schemas():
    # Test ContributionCreate
    contribution_data = {
        "member_id": 1,
        "project_id": 1,
        "amount": 1000.0,
        "payment_method": PaymentMethod.CASH,
        "payment_date": datetime.now(),
        "notes": "Test contribution"
    }
    contribution_create = ContributionCreate(**contribution_data)
    assert contribution_create.member_id == contribution_data["member_id"]
    assert contribution_create.project_id == contribution_data["project_id"]
    assert contribution_create.amount == contribution_data["amount"]
    assert contribution_create.payment_method == contribution_data["payment_method"]
    assert contribution_create.payment_date == contribution_data["payment_date"]
    assert contribution_create.notes == contribution_data["notes"]
    
    # Test ContributionUpdate
    update_data = {
        "amount": 2000.0,
        "payment_method": PaymentMethod.BANK_TRANSFER
    }
    contribution_update = ContributionUpdate(**update_data)
    assert contribution_update.amount == update_data["amount"]
    assert contribution_update.payment_method == update_data["payment_method"]
    
    # Test validation
    with pytest.raises(ValueError):
        ContributionCreate(
            member_id=1,
            project_id=1,
            amount=-1000.0,
            payment_method=PaymentMethod.CASH,
            payment_date=datetime.now()
        )

def test_sms_schemas():
    # Test SMSRequest
    sms_data = {
        "phone_number": "+1234567890",
        "message": "Test SMS message"
    }
    sms_request = SMSRequest(**sms_data)
    assert sms_request.phone_number == sms_data["phone_number"]
    assert sms_request.message == sms_data["message"]
    
    # Test SMSResponse
    response_data = {
        "message_id": "test123",
        "status": "QUEUED",
        "sent_at": datetime.now(),
        "delivered_at": None
    }
    sms_response = SMSResponse(**response_data)
    assert sms_response.message_id == response_data["message_id"]
    assert sms_response.status == response_data["status"]
    assert sms_response.sent_at == response_data["sent_at"]
    assert sms_response.delivered_at == response_data["delivered_at"]
    
    # Test validation
    with pytest.raises(ValueError):
        SMSRequest(phone_number="invalid", message="Test")
    
    with pytest.raises(ValueError):
        SMSRequest(phone_number="+1234567890", message="")

def test_schema_inheritance():
    # Test that all schemas inherit from BaseModel
    from pydantic import BaseModel
    
    assert issubclass(UserCreate, BaseModel)
    assert issubclass(UserUpdate, BaseModel)
    assert issubclass(MemberCreate, BaseModel)
    assert issubclass(MemberUpdate, BaseModel)
    assert issubclass(GroupCreate, BaseModel)
    assert issubclass(GroupUpdate, BaseModel)
    assert issubclass(ProjectCreate, BaseModel)
    assert issubclass(ProjectUpdate, BaseModel)
    assert issubclass(ContributionCreate, BaseModel)
    assert issubclass(ContributionUpdate, BaseModel)
    assert issubclass(SMSRequest, BaseModel)
    assert issubclass(SMSResponse, BaseModel)

def test_schema_optional_fields():
    # Test that update schemas have optional fields
    from typing import Optional
    
    assert Optional[str] == UserUpdate.__annotations__.get("full_name")
    assert Optional[UserRole] == UserUpdate.__annotations__.get("role")
    assert Optional[str] == MemberUpdate.__annotations__.get("name")
    assert Optional[str] == MemberUpdate.__annotations__.get("alias")
    assert Optional[str] == GroupUpdate.__annotations__.get("name")
    assert Optional[list] == GroupUpdate.__annotations__.get("member_ids")
    assert Optional[float] == ProjectUpdate.__annotations__.get("target_amount")
    assert Optional[datetime] == ProjectUpdate.__annotations__.get("end_date")
    assert Optional[float] == ContributionUpdate.__annotations__.get("amount")
    assert Optional[str] == ContributionUpdate.__annotations__.get("notes") 