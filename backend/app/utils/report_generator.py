import os
import pandas as pd
from sqlalchemy.orm import Session
from app.models.contribution import Contribution
from app.models.project import Project
from app.models.member import Member
from app.models.group import Group
from typing import List, Optional
from datetime import datetime
from sqlalchemy import func

def generate_project_report(
    db: Session,
    project_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> pd.DataFrame:
    """Generate a report for a specific project"""
    query = db.query(
        Contribution,
        Member,
        Group
    ).join(
        Member, Contribution.member_id == Member.id
    ).outerjoin(
        Group, Contribution.group_id == Group.id
    ).filter(
        Contribution.project_id == project_id
    )
    
    if start_date:
        query = query.filter(Contribution.created_at >= start_date)
    if end_date:
        query = query.filter(Contribution.created_at <= end_date)
    
    results = query.all()
    
    data = []
    for contribution, member, group in results:
        data.append({
            "Date": contribution.created_at,
            "Member Code": member.code,
            "Member Name": member.name,
            "Group": group.name if group else "Individual",
            "Type": contribution.type,
            "Amount": contribution.amount,
            "Status": "Completed" if contribution.type == "contribution" else "Pending"
        })
    
    return pd.DataFrame(data)

def generate_group_report(
    db: Session,
    group_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> pd.DataFrame:
    """Generate a report for a specific group"""
    query = db.query(
        Contribution,
        Member,
        Project
    ).join(
        Member, Contribution.member_id == Member.id
    ).join(
        Project, Contribution.project_id == Project.id
    ).filter(
        Contribution.group_id == group_id
    )
    
    if start_date:
        query = query.filter(Contribution.created_at >= start_date)
    if end_date:
        query = query.filter(Contribution.created_at <= end_date)
    
    results = query.all()
    
    data = []
    for contribution, member, project in results:
        data.append({
            "Date": contribution.created_at,
            "Member Code": member.code,
            "Member Name": member.name,
            "Project": project.name,
            "Type": contribution.type,
            "Amount": contribution.amount,
            "Status": "Completed" if contribution.type == "contribution" else "Pending"
        })
    
    return pd.DataFrame(data)

def generate_member_report(
    db: Session,
    member_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> pd.DataFrame:
    """Generate a report for a specific member"""
    query = db.query(
        Contribution,
        Project,
        Group
    ).join(
        Project, Contribution.project_id == Project.id
    ).outerjoin(
        Group, Contribution.group_id == Group.id
    ).filter(
        Contribution.member_id == member_id
    )
    
    if start_date:
        query = query.filter(Contribution.created_at >= start_date)
    if end_date:
        query = query.filter(Contribution.created_at <= end_date)
    
    results = query.all()
    
    data = []
    for contribution, project, group in results:
        data.append({
            "Date": contribution.created_at,
            "Project": project.name,
            "Group": group.name if group else "Individual",
            "Type": contribution.type,
            "Amount": contribution.amount,
            "Status": "Completed" if contribution.type == "contribution" else "Pending"
        })
    
    return pd.DataFrame(data)

def save_report_to_excel(df: pd.DataFrame, filename: str) -> Optional[str]:
    """
    Save a pandas DataFrame to an Excel file.
    """
    try:
        # Create reports directory if it doesn't exist
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        filepath = os.path.join(reports_dir, filename)
        df.to_excel(filepath, index=False)
        return filepath
    except Exception as e:
        print(f"Error saving report to Excel: {str(e)}")
        return None 