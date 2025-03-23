from typing import Generator
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app import crud
from app.models.member import Member
from app.models.project import Project
from app.models.group import Group
from app.models.contribution import Contribution
from app.schemas.member import MemberCreate
from app.schemas.project import ProjectCreate
from app.schemas.group import GroupCreate
from app.schemas.contribution import ContributionCreate, ContributionUpdate

def test_create_contribution(db: Session) -> None:
    # Create a member
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    
    # Create a project
    project_in = ProjectCreate(
        name="Test Project",
        description="Test Project Description",
        target_amount=10000.0,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        status="active",
    )
    project = crud.project.create(db, obj_in=project_in)
    
    # Create a contribution
    contribution_in = ContributionCreate(
        member_id=member.id,
        project_id=project.id,
        amount=1000.0,
        type="contribution",
    )
    contribution = crud.contribution.create(db, obj_in=contribution_in)
    assert contribution.member_id == member.id
    assert contribution.project_id == project.id
    assert contribution.amount == 1000.0
    assert contribution.type == "contribution"

def test_create_contribution_with_group(db: Session) -> None:
    # Create a member
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    
    # Create a project
    project_in = ProjectCreate(
        name="Test Project",
        description="Test Project Description",
        target_amount=10000.0,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        status="active",
    )
    project = crud.project.create(db, obj_in=project_in)
    
    # Create a group
    group_in = GroupCreate(
        name="Test Group",
        description="Test Group Description",
    )
    group = crud.group.create(db, obj_in=group_in)
    
    # Add member to group
    crud.group.add_member(db, group_id=group.id, member_id=member.id)
    
    # Create a contribution
    contribution_in = ContributionCreate(
        member_id=member.id,
        project_id=project.id,
        group_id=group.id,
        amount=1000.0,
        type="contribution",
    )
    contribution = crud.contribution.create(db, obj_in=contribution_in)
    assert contribution.member_id == member.id
    assert contribution.project_id == project.id
    assert contribution.group_id == group.id
    assert contribution.amount == 1000.0
    assert contribution.type == "contribution"

def test_get_contribution(db: Session) -> None:
    # Create a member
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    
    # Create a project
    project_in = ProjectCreate(
        name="Test Project",
        description="Test Project Description",
        target_amount=10000.0,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        status="active",
    )
    project = crud.project.create(db, obj_in=project_in)
    
    # Create a contribution
    contribution_in = ContributionCreate(
        member_id=member.id,
        project_id=project.id,
        amount=1000.0,
        type="contribution",
    )
    contribution = crud.contribution.create(db, obj_in=contribution_in)
    
    # Get the contribution
    stored_contribution = crud.contribution.get(db, id=contribution.id)
    assert stored_contribution
    assert contribution.id == stored_contribution.id
    assert contribution.member_id == stored_contribution.member_id
    assert contribution.project_id == stored_contribution.project_id
    assert contribution.amount == stored_contribution.amount
    assert contribution.type == stored_contribution.type

def test_get_contribution_by_member(db: Session) -> None:
    # Create a member
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    
    # Create a project
    project_in = ProjectCreate(
        name="Test Project",
        description="Test Project Description",
        target_amount=10000.0,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        status="active",
    )
    project = crud.project.create(db, obj_in=project_in)
    
    # Create a contribution
    contribution_in = ContributionCreate(
        member_id=member.id,
        project_id=project.id,
        amount=1000.0,
        type="contribution",
    )
    contribution = crud.contribution.create(db, obj_in=contribution_in)
    
    # Get contributions by member
    stored_contributions = crud.contribution.get_by_member(db, member_id=member.id)
    assert len(stored_contributions) > 0
    assert any(c.id == contribution.id for c in stored_contributions)

def test_get_contribution_by_project(db: Session) -> None:
    # Create a member
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    
    # Create a project
    project_in = ProjectCreate(
        name="Test Project",
        description="Test Project Description",
        target_amount=10000.0,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        status="active",
    )
    project = crud.project.create(db, obj_in=project_in)
    
    # Create a contribution
    contribution_in = ContributionCreate(
        member_id=member.id,
        project_id=project.id,
        amount=1000.0,
        type="contribution",
    )
    contribution = crud.contribution.create(db, obj_in=contribution_in)
    
    # Get contributions by project
    stored_contributions = crud.contribution.get_by_project(db, project_id=project.id)
    assert len(stored_contributions) > 0
    assert any(c.id == contribution.id for c in stored_contributions)

def test_get_contribution_by_group(db: Session) -> None:
    # Create a member
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    
    # Create a project
    project_in = ProjectCreate(
        name="Test Project",
        description="Test Project Description",
        target_amount=10000.0,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        status="active",
    )
    project = crud.project.create(db, obj_in=project_in)
    
    # Create a group
    group_in = GroupCreate(
        name="Test Group",
        description="Test Group Description",
    )
    group = crud.group.create(db, obj_in=group_in)
    
    # Add member to group
    crud.group.add_member(db, group_id=group.id, member_id=member.id)
    
    # Create a contribution
    contribution_in = ContributionCreate(
        member_id=member.id,
        project_id=project.id,
        group_id=group.id,
        amount=1000.0,
        type="contribution",
    )
    contribution = crud.contribution.create(db, obj_in=contribution_in)
    
    # Get contributions by group
    stored_contributions = crud.contribution.get_by_group(db, group_id=group.id)
    assert len(stored_contributions) > 0
    assert any(c.id == contribution.id for c in stored_contributions)

def test_update_contribution(db: Session) -> None:
    # Create a member
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    
    # Create a project
    project_in = ProjectCreate(
        name="Test Project",
        description="Test Project Description",
        target_amount=10000.0,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        status="active",
    )
    project = crud.project.create(db, obj_in=project_in)
    
    # Create a contribution
    contribution_in = ContributionCreate(
        member_id=member.id,
        project_id=project.id,
        amount=1000.0,
        type="contribution",
    )
    contribution = crud.contribution.create(db, obj_in=contribution_in)
    
    # Update the contribution
    contribution_in_update = ContributionUpdate(
        amount=2000.0,
        type="pledge",
    )
    contribution2 = crud.contribution.update(db, db_obj=contribution, obj_in=contribution_in_update)
    assert contribution.id == contribution2.id
    assert contribution2.amount == 2000.0
    assert contribution2.type == "pledge"
    assert contribution2.member_id == member.id
    assert contribution2.project_id == project.id

def test_get_total_contributed(db: Session) -> None:
    # Create a member
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    
    # Create a project
    project_in = ProjectCreate(
        name="Test Project",
        description="Test Project Description",
        target_amount=10000.0,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        status="active",
    )
    project = crud.project.create(db, obj_in=project_in)
    
    # Create contributions
    contribution_in1 = ContributionCreate(
        member_id=member.id,
        project_id=project.id,
        amount=1000.0,
        type="contribution",
    )
    contribution_in2 = ContributionCreate(
        member_id=member.id,
        project_id=project.id,
        amount=2000.0,
        type="contribution",
    )
    crud.contribution.create(db, obj_in=contribution_in1)
    crud.contribution.create(db, obj_in=contribution_in2)
    
    # Get total contributed
    total = crud.contribution.get_total_contributed(db, project_id=project.id)
    assert total == 3000.0

def test_get_total_pledged(db: Session) -> None:
    # Create a member
    member_in = MemberCreate(
        name="Test Member",
        phone_number="1234567890",
        alias="TM",
        is_active=True,
    )
    member = crud.member.create(db, obj_in=member_in)
    
    # Create a project
    project_in = ProjectCreate(
        name="Test Project",
        description="Test Project Description",
        target_amount=10000.0,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        status="active",
    )
    project = crud.project.create(db, obj_in=project_in)
    
    # Create pledges
    pledge_in1 = ContributionCreate(
        member_id=member.id,
        project_id=project.id,
        amount=1000.0,
        type="pledge",
    )
    pledge_in2 = ContributionCreate(
        member_id=member.id,
        project_id=project.id,
        amount=2000.0,
        type="pledge",
    )
    crud.contribution.create(db, obj_in=pledge_in1)
    crud.contribution.create(db, obj_in=pledge_in2)
    
    # Get total pledged
    total = crud.contribution.get_total_pledged(db, project_id=project.id)
    assert total == 3000.0 