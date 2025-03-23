import pytest
from datetime import datetime, timedelta
from app.models.user import User
from app.models.member import Member
from app.models.group import Group
from app.models.project import Project
from app.models.contribution import Contribution
from app.models.sms import SMS
from app.schemas.user import UserRole
from app.schemas.contribution import PaymentMethod

def test_user_model(db):
    # Create a user
    user = User(
        email="test@example.com",
        hashed_password="test_hash",
        full_name="Test User",
        role=UserRole.STAFF
    )
    db.add(user)
    db.commit()
    
    # Retrieve the user
    retrieved_user = db.query(User).filter(User.email == "test@example.com").first()
    assert retrieved_user is not None
    assert retrieved_user.email == "test@example.com"
    assert retrieved_user.full_name == "Test User"
    assert retrieved_user.role == UserRole.STAFF
    assert retrieved_user.is_active == True
    assert retrieved_user.created_at is not None
    assert retrieved_user.updated_at is not None

def test_member_model(db):
    # Create a member
    member = Member(
        name="Test Member",
        alias="TM",
        phone_number="+1234567890",
        unique_code="ABC123"
    )
    db.add(member)
    db.commit()
    
    # Retrieve the member
    retrieved_member = db.query(Member).filter(Member.phone_number == "+1234567890").first()
    assert retrieved_member is not None
    assert retrieved_member.name == "Test Member"
    assert retrieved_member.alias == "TM"
    assert retrieved_member.phone_number == "+1234567890"
    assert retrieved_member.unique_code == "ABC123"
    assert retrieved_member.created_at is not None
    assert retrieved_member.updated_at is not None

def test_group_model(db, test_member):
    # Create a group
    group = Group(
        name="Test Group",
        description="Test group description"
    )
    group.members.append(test_member)
    db.add(group)
    db.commit()
    
    # Retrieve the group
    retrieved_group = db.query(Group).filter(Group.name == "Test Group").first()
    assert retrieved_group is not None
    assert retrieved_group.name == "Test Group"
    assert retrieved_group.description == "Test group description"
    assert len(retrieved_group.members) == 1
    assert retrieved_group.members[0].id == test_member.id
    assert retrieved_group.created_at is not None
    assert retrieved_group.updated_at is not None

def test_project_model(db):
    # Create a project
    project = Project(
        name="Test Project",
        description="Test project description",
        target_amount=10000.0,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30)
    )
    db.add(project)
    db.commit()
    
    # Retrieve the project
    retrieved_project = db.query(Project).filter(Project.name == "Test Project").first()
    assert retrieved_project is not None
    assert retrieved_project.name == "Test Project"
    assert retrieved_project.description == "Test project description"
    assert retrieved_project.target_amount == 10000.0
    assert retrieved_project.start_date is not None
    assert retrieved_project.end_date is not None
    assert retrieved_project.created_at is not None
    assert retrieved_project.updated_at is not None

def test_contribution_model(db, test_member, test_project):
    # Create a contribution
    contribution = Contribution(
        member_id=test_member.id,
        project_id=test_project.id,
        amount=1000.0,
        payment_method=PaymentMethod.CASH,
        payment_date=datetime.now(),
        notes="Test contribution"
    )
    db.add(contribution)
    db.commit()
    
    # Retrieve the contribution
    retrieved_contribution = db.query(Contribution).filter(Contribution.id == contribution.id).first()
    assert retrieved_contribution is not None
    assert retrieved_contribution.amount == 1000.0
    assert retrieved_contribution.payment_method == PaymentMethod.CASH
    assert retrieved_contribution.payment_date is not None
    assert retrieved_contribution.notes == "Test contribution"
    assert retrieved_contribution.member_id == test_member.id
    assert retrieved_contribution.project_id == test_project.id
    assert retrieved_contribution.created_at is not None
    assert retrieved_contribution.updated_at is not None

def test_sms_model(db, test_member):
    # Create an SMS
    sms = SMS(
        phone_number=test_member.phone_number,
        message="Test SMS message",
        status="QUEUED"
    )
    db.add(sms)
    db.commit()
    
    # Retrieve the SMS
    retrieved_sms = db.query(SMS).filter(SMS.id == sms.id).first()
    assert retrieved_sms is not None
    assert retrieved_sms.phone_number == test_member.phone_number
    assert retrieved_sms.message == "Test SMS message"
    assert retrieved_sms.status == "QUEUED"
    assert retrieved_sms.created_at is not None
    assert retrieved_sms.updated_at is not None

def test_model_relationships(db, test_member, test_project):
    # Create a contribution linking member and project
    contribution = Contribution(
        member_id=test_member.id,
        project_id=test_project.id,
        amount=1000.0,
        payment_method=PaymentMethod.CASH,
        payment_date=datetime.now()
    )
    db.add(contribution)
    db.commit()
    
    # Test member -> contributions relationship
    member_contributions = test_member.contributions
    assert len(member_contributions) == 1
    assert member_contributions[0].id == contribution.id
    
    # Test project -> contributions relationship
    project_contributions = test_project.contributions
    assert len(project_contributions) == 1
    assert project_contributions[0].id == contribution.id

def test_model_cascade_delete(db, test_member, test_project):
    # Create a contribution
    contribution = Contribution(
        member_id=test_member.id,
        project_id=test_project.id,
        amount=1000.0,
        payment_method=PaymentMethod.CASH,
        payment_date=datetime.now()
    )
    db.add(contribution)
    db.commit()
    
    # Delete the member
    db.delete(test_member)
    db.commit()
    
    # Verify contribution is deleted
    deleted_contribution = db.query(Contribution).filter(Contribution.id == contribution.id).first()
    assert deleted_contribution is None

def test_model_timestamps(db, test_member):
    # Get initial timestamps
    created_at = test_member.created_at
    updated_at = test_member.updated_at
    
    # Update the member
    test_member.name = "Updated Name"
    db.commit()
    
    # Verify timestamps
    assert test_member.created_at == created_at
    assert test_member.updated_at > updated_at

def test_model_constraints(db):
    # Test unique email constraint
    user1 = User(
        email="test@example.com",
        hashed_password="test_hash",
        full_name="Test User 1"
    )
    db.add(user1)
    db.commit()
    
    user2 = User(
        email="test@example.com",
        hashed_password="test_hash",
        full_name="Test User 2"
    )
    db.add(user2)
    with pytest.raises(Exception):
        db.commit()
    
    # Test unique phone number constraint
    member1 = Member(
        name="Test Member 1",
        phone_number="+1234567890",
        unique_code="ABC123"
    )
    db.add(member1)
    db.commit()
    
    member2 = Member(
        name="Test Member 2",
        phone_number="+1234567890",
        unique_code="DEF456"
    )
    db.add(member2)
    with pytest.raises(Exception):
        db.commit() 