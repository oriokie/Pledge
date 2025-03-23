import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import os
from app.services.storage_service import StorageService
from app.core.exceptions import StorageError

@pytest.fixture
def storage_service():
    """Create storage service instance"""
    return StorageService()

@pytest.fixture
def mock_local_storage():
    """Mock local storage backend"""
    with patch("app.services.storage_service.LocalStorage") as mock:
        mock_instance = MagicMock()
        mock_instance.upload_file.return_value = {"url": "file:///local/path/file.pdf"}
        mock_instance.download_file.return_value = b"file content"
        mock.return_value = mock_instance
        yield mock

@pytest.fixture
def mock_s3_storage():
    """Mock S3 storage backend"""
    with patch("app.services.storage_service.S3Storage") as mock:
        mock_instance = MagicMock()
        mock_instance.upload_file.return_value = {"url": "https://s3.amazonaws.com/bucket/file.pdf"}
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

def test_upload_file_local_success(storage_service, mock_local_storage, test_file):
    """Test successful file upload to local storage"""
    # Test data
    file_name, file_content = test_file
    
    # Upload file
    result = storage_service.upload_file(file_name, file_content, backend="local")
    
    # Verify result
    assert result["status"] == "success"
    assert "url" in result
    assert result["url"].startswith("file:///")
    
    # Verify local storage was called
    mock_local_storage.return_value.upload_file.assert_called_once()

def test_upload_file_s3_success(storage_service, mock_s3_storage, test_file):
    """Test successful file upload to S3 storage"""
    # Test data
    file_name, file_content = test_file
    
    # Upload file
    result = storage_service.upload_file(file_name, file_content, backend="s3")
    
    # Verify result
    assert result["status"] == "success"
    assert "url" in result
    assert result["url"].startswith("https://s3.amazonaws.com/")
    
    # Verify S3 storage was called
    mock_s3_storage.return_value.upload_file.assert_called_once()

def test_upload_file_failure(storage_service, mock_local_storage):
    """Test failed file upload"""
    # Configure mock to raise exception
    mock_local_storage.return_value.upload_file.side_effect = Exception("Storage error")
    
    # Test data
    file_name = "test.pdf"
    file_content = b"test content"
    
    # Upload file
    with pytest.raises(StorageError) as exc_info:
        storage_service.upload_file(file_name, file_content, backend="local")
    
    # Verify error
    assert str(exc_info.value) == "Failed to upload file: Storage error"

def test_download_file_local_success(storage_service, mock_local_storage):
    """Test successful file download from local storage"""
    # Test data
    file_url = "file:///local/path/file.pdf"
    
    # Download file
    result = storage_service.download_file(file_url, backend="local")
    
    # Verify result
    assert result["status"] == "success"
    assert "content" in result
    assert result["content"] == b"file content"
    
    # Verify local storage was called
    mock_local_storage.return_value.download_file.assert_called_once_with(file_url)

def test_download_file_s3_success(storage_service, mock_s3_storage):
    """Test successful file download from S3 storage"""
    # Test data
    file_url = "https://s3.amazonaws.com/bucket/file.pdf"
    
    # Download file
    result = storage_service.download_file(file_url, backend="s3")
    
    # Verify result
    assert result["status"] == "success"
    assert "content" in result
    assert result["content"] == b"file content"
    
    # Verify S3 storage was called
    mock_s3_storage.return_value.download_file.assert_called_once_with(file_url)

def test_download_file_failure(storage_service, mock_local_storage):
    """Test failed file download"""
    # Configure mock to raise exception
    mock_local_storage.return_value.download_file.side_effect = Exception("Storage error")
    
    # Test data
    file_url = "file:///local/path/file.pdf"
    
    # Download file
    with pytest.raises(StorageError) as exc_info:
        storage_service.download_file(file_url, backend="local")
    
    # Verify error
    assert str(exc_info.value) == "Failed to download file: Storage error"

def test_delete_file_local_success(storage_service, mock_local_storage):
    """Test successful file deletion from local storage"""
    # Test data
    file_url = "file:///local/path/file.pdf"
    
    # Delete file
    result = storage_service.delete_file(file_url, backend="local")
    
    # Verify result
    assert result["status"] == "success"
    
    # Verify local storage was called
    mock_local_storage.return_value.delete_file.assert_called_once_with(file_url)

def test_delete_file_s3_success(storage_service, mock_s3_storage):
    """Test successful file deletion from S3 storage"""
    # Test data
    file_url = "https://s3.amazonaws.com/bucket/file.pdf"
    
    # Delete file
    result = storage_service.delete_file(file_url, backend="s3")
    
    # Verify result
    assert result["status"] == "success"
    
    # Verify S3 storage was called
    mock_s3_storage.return_value.delete_file.assert_called_once_with(file_url)

def test_delete_file_failure(storage_service, mock_local_storage):
    """Test failed file deletion"""
    # Configure mock to raise exception
    mock_local_storage.return_value.delete_file.side_effect = Exception("Storage error")
    
    # Test data
    file_url = "file:///local/path/file.pdf"
    
    # Delete file
    with pytest.raises(StorageError) as exc_info:
        storage_service.delete_file(file_url, backend="local")
    
    # Verify error
    assert str(exc_info.value) == "Failed to delete file: Storage error"

def test_get_file_url(storage_service):
    """Test getting file URL"""
    # Test data
    file_name = "test.pdf"
    
    # Get URLs for different backends
    local_url = storage_service.get_file_url(file_name, backend="local")
    s3_url = storage_service.get_file_url(file_name, backend="s3")
    
    # Verify URLs
    assert local_url.startswith("file:///")
    assert s3_url.startswith("https://s3.amazonaws.com/")

def test_validate_backend(storage_service):
    """Test backend validation"""
    # Valid backends
    assert storage_service.validate_backend("local") is True
    assert storage_service.validate_backend("s3") is True
    
    # Invalid backend
    assert storage_service.validate_backend("invalid") is False

def test_get_storage_backend(storage_service):
    """Test getting storage backend"""
    # Test data
    file_urls = [
        "file:///local/path/file.pdf",
        "https://s3.amazonaws.com/bucket/file.pdf",
        "invalid://url/file.pdf"
    ]
    
    # Get backends
    backends = [storage_service.get_storage_backend(url) for url in file_urls]
    
    # Verify backends
    assert backends == ["local", "s3", None] 