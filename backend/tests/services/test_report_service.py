import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from app.services.report_service import ReportService
from app.models.contribution import Contribution
from app.models.project import Project
from app.models.member import Member
from app.models.group import Group
from app.core.exceptions import ReportError

@pytest.fixture
def report_service():
    """Create report service instance"""
    return ReportService()

@pytest.fixture
def mock_db():
    """Mock database session"""
    with patch("app.services.report_service.get_db") as mock:
        mock_db = MagicMock()
        mock.return_value = mock_db
        yield mock_db

def test_generate_daily_report(report_service, mock_db):
    """Test daily report generation"""
    # Test data
    date = datetime.now().date()
    mock_db.query.return_value.filter.return_value.all.return_value = [
        Contribution(id=1, amount=1000, created_at=datetime.now()),
        Contribution(id=2, amount=2000, created_at=datetime.now())
    ]
    
    # Generate report
    report = report_service.generate_daily_report(date)
    
    # Verify report structure
    assert "total_amount" in report
    assert "contribution_count" in report
    assert "contributions" in report
    
    # Verify report data
    assert report["total_amount"] == 3000
    assert report["contribution_count"] == 2
    assert len(report["contributions"]) == 2

def test_generate_weekly_report(report_service, mock_db):
    """Test weekly report generation"""
    # Test data
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=6)
    mock_db.query.return_value.filter.return_value.all.return_value = [
        Contribution(id=1, amount=1000, created_at=datetime.now()),
        Contribution(id=2, amount=2000, created_at=datetime.now())
    ]
    
    # Generate report
    report = report_service.generate_weekly_report(start_date, end_date)
    
    # Verify report structure
    assert "total_amount" in report
    assert "contribution_count" in report
    assert "daily_breakdown" in report
    
    # Verify report data
    assert report["total_amount"] == 3000
    assert report["contribution_count"] == 2
    assert len(report["daily_breakdown"]) == 7

def test_generate_monthly_report(report_service, mock_db):
    """Test monthly report generation"""
    # Test data
    year = 2024
    month = 1
    mock_db.query.return_value.filter.return_value.all.return_value = [
        Contribution(id=1, amount=1000, created_at=datetime.now()),
        Contribution(id=2, amount=2000, created_at=datetime.now())
    ]
    
    # Generate report
    report = report_service.generate_monthly_report(year, month)
    
    # Verify report structure
    assert "total_amount" in report
    assert "contribution_count" in report
    assert "weekly_breakdown" in report
    
    # Verify report data
    assert report["total_amount"] == 3000
    assert report["contribution_count"] == 2
    assert len(report["weekly_breakdown"]) == 4

def test_generate_project_report(report_service, mock_db):
    """Test project report generation"""
    # Test data
    project_id = 1
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=30)
    mock_db.query.return_value.filter.return_value.all.return_value = [
        Contribution(id=1, amount=1000, created_at=datetime.now()),
        Contribution(id=2, amount=2000, created_at=datetime.now())
    ]
    
    # Generate report
    report = report_service.generate_project_report(project_id, start_date, end_date)
    
    # Verify report structure
    assert "project_details" in report
    assert "total_amount" in report
    assert "contribution_count" in report
    assert "contributions" in report
    
    # Verify report data
    assert report["total_amount"] == 3000
    assert report["contribution_count"] == 2
    assert len(report["contributions"]) == 2

def test_generate_member_report(report_service, mock_db):
    """Test member report generation"""
    # Test data
    member_id = 1
    mock_db.query.return_value.filter.return_value.all.return_value = [
        Contribution(id=1, amount=1000, created_at=datetime.now()),
        Contribution(id=2, amount=2000, created_at=datetime.now())
    ]
    
    # Generate report
    report = report_service.generate_member_report(member_id)
    
    # Verify report structure
    assert "member_details" in report
    assert "total_amount" in report
    assert "contribution_count" in report
    assert "contributions" in report
    
    # Verify report data
    assert report["total_amount"] == 3000
    assert report["contribution_count"] == 2
    assert len(report["contributions"]) == 2

def test_generate_group_report(report_service, mock_db):
    """Test group report generation"""
    # Test data
    group_id = 1
    mock_db.query.return_value.filter.return_value.all.return_value = [
        Contribution(id=1, amount=1000, created_at=datetime.now()),
        Contribution(id=2, amount=2000, created_at=datetime.now())
    ]
    
    # Generate report
    report = report_service.generate_group_report(group_id)
    
    # Verify report structure
    assert "group_details" in report
    assert "total_amount" in report
    assert "contribution_count" in report
    assert "member_breakdown" in report
    
    # Verify report data
    assert report["total_amount"] == 3000
    assert report["contribution_count"] == 2
    assert "member_breakdown" in report

def test_export_report_to_excel(report_service):
    """Test report export to Excel"""
    # Test data
    report_data = {
        "total_amount": 3000,
        "contribution_count": 2,
        "contributions": [
            {"id": 1, "amount": 1000},
            {"id": 2, "amount": 2000}
        ]
    }
    
    # Export report
    file_path = report_service.export_report_to_excel(report_data, "test_report")
    
    # Verify file was created
    assert file_path.endswith(".xlsx")
    
    # Clean up
    import os
    if os.path.exists(file_path):
        os.remove(file_path)

def test_export_report_to_pdf(report_service):
    """Test report export to PDF"""
    # Test data
    report_data = {
        "total_amount": 3000,
        "contribution_count": 2,
        "contributions": [
            {"id": 1, "amount": 1000},
            {"id": 2, "amount": 2000}
        ]
    }
    
    # Export report
    file_path = report_service.export_report_to_pdf(report_data, "test_report")
    
    # Verify file was created
    assert file_path.endswith(".pdf")
    
    # Clean up
    import os
    if os.path.exists(file_path):
        os.remove(file_path)

def test_report_error_handling(report_service, mock_db):
    """Test report error handling"""
    # Configure mock to raise exception
    mock_db.query.return_value.filter.return_value.all.side_effect = Exception("Database error")
    
    # Test data
    date = datetime.now().date()
    
    # Generate report
    with pytest.raises(ReportError) as exc_info:
        report_service.generate_daily_report(date)
    
    # Verify error
    assert str(exc_info.value) == "Failed to generate report: Database error" 