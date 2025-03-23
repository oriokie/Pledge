import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import os
from app.services.file_service import FileService
from app.core.exceptions import FileError

@pytest.fixture
def file_service():
    """Create file service instance"""
    return FileService()

@pytest.fixture
def mock_storage():
    """Mock storage service"""
    with patch("app.services.file_service.StorageService") as mock:
        mock_instance = MagicMock()
        mock_instance.upload_file.return_value = {"url": "https://example.com/file.pdf"}
        mock_instance.download_file.return_value = b"file content"
        mock.return_value = mock_instance
        yield mock

@pytest.fixture
def test_file():
    """Create a test file"""
    file_content = b"test file content"
    file_name = "test.pdf"
    
    # Create temporary file
    with open(file_name, "wb") as f:
        f.write(file_content)
    
    yield file_name, file_content
    
    # Clean up
    if os.path.exists(file_name):
        os.remove(file_name)

def test_upload_file_success(file_service, mock_storage, test_file):
    """Test successful file upload"""
    # Test data
    file_name, file_content = test_file
    
    # Upload file
    result = file_service.upload_file(file_name, file_content)
    
    # Verify result
    assert result["status"] == "success"
    assert "url" in result
    assert result["url"] == "https://example.com/file.pdf"
    
    # Verify storage was called
    mock_storage.return_value.upload_file.assert_called_once()

def test_upload_file_failure(file_service, mock_storage):
    """Test failed file upload"""
    # Configure mock to raise exception
    mock_storage.return_value.upload_file.side_effect = Exception("Storage error")
    
    # Test data
    file_name = "test.pdf"
    file_content = b"test content"
    
    # Upload file
    with pytest.raises(FileError) as exc_info:
        file_service.upload_file(file_name, file_content)
    
    # Verify error
    assert str(exc_info.value) == "Failed to upload file: Storage error"

def test_download_file_success(file_service, mock_storage):
    """Test successful file download"""
    # Test data
    file_url = "https://example.com/file.pdf"
    
    # Download file
    result = file_service.download_file(file_url)
    
    # Verify result
    assert result["status"] == "success"
    assert "content" in result
    assert result["content"] == b"file content"
    
    # Verify storage was called
    mock_storage.return_value.download_file.assert_called_once_with(file_url)

def test_download_file_failure(file_service, mock_storage):
    """Test failed file download"""
    # Configure mock to raise exception
    mock_storage.return_value.download_file.side_effect = Exception("Storage error")
    
    # Test data
    file_url = "https://example.com/file.pdf"
    
    # Download file
    with pytest.raises(FileError) as exc_info:
        file_service.download_file(file_url)
    
    # Verify error
    assert str(exc_info.value) == "Failed to download file: Storage error"

def test_delete_file_success(file_service, mock_storage):
    """Test successful file deletion"""
    # Test data
    file_url = "https://example.com/file.pdf"
    
    # Delete file
    result = file_service.delete_file(file_url)
    
    # Verify result
    assert result["status"] == "success"
    
    # Verify storage was called
    mock_storage.return_value.delete_file.assert_called_once_with(file_url)

def test_delete_file_failure(file_service, mock_storage):
    """Test failed file deletion"""
    # Configure mock to raise exception
    mock_storage.return_value.delete_file.side_effect = Exception("Storage error")
    
    # Test data
    file_url = "https://example.com/file.pdf"
    
    # Delete file
    with pytest.raises(FileError) as exc_info:
        file_service.delete_file(file_url)
    
    # Verify error
    assert str(exc_info.value) == "Failed to delete file: Storage error"

def test_validate_file_type(file_service):
    """Test file type validation"""
    # Valid file types
    assert file_service.validate_file_type("test.pdf", ["pdf", "doc", "docx"]) is True
    assert file_service.validate_file_type("test.docx", ["pdf", "doc", "docx"]) is True
    
    # Invalid file types
    assert file_service.validate_file_type("test.txt", ["pdf", "doc", "docx"]) is False
    assert file_service.validate_file_type("test", ["pdf", "doc", "docx"]) is False

def test_validate_file_size(file_service):
    """Test file size validation"""
    # Valid file size (5MB)
    assert file_service.validate_file_size(5 * 1024 * 1024, max_size=10 * 1024 * 1024) is True
    
    # Invalid file size (15MB)
    assert file_service.validate_file_size(15 * 1024 * 1024, max_size=10 * 1024 * 1024) is False

def test_generate_file_name(file_service):
    """Test file name generation"""
    # Test data
    original_name = "test.pdf"
    
    # Generate file name
    new_name = file_service.generate_file_name(original_name)
    
    # Verify name
    assert new_name.endswith(".pdf")
    assert len(new_name) > len(original_name)
    
    # Test uniqueness
    names = [file_service.generate_file_name(original_name) for _ in range(100)]
    assert len(set(names)) == 100

def test_get_file_extension(file_service):
    """Test getting file extension"""
    # Test data
    file_names = [
        "test.pdf",
        "document.docx",
        "image.jpg",
        "file",
        "test.tar.gz"
    ]
    
    # Get extensions
    extensions = [file_service.get_file_extension(name) for name in file_names]
    
    # Verify extensions
    assert extensions == ["pdf", "docx", "jpg", "", "gz"]

def test_clean_file_name(file_service):
    """Test file name cleaning"""
    # Test data
    file_names = [
        "Test File.pdf",
        "user's document.docx",
        "file with spaces.jpg",
        "file@#$%.txt"
    ]
    
    # Clean names
    cleaned_names = [file_service.clean_file_name(name) for name in file_names]
    
    # Verify cleaned names
    assert cleaned_names == [
        "test_file.pdf",
        "users_document.docx",
        "file_with_spaces.jpg",
        "file.txt"
    ] 