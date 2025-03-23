from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.deps import get_db
from ....services.storage_service import StorageService
from ....schemas.file import FileResponse, FileListResponse

router = APIRouter()

@router.post("/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    entity_type: str = None,
    entity_id: int = None,
    db: Session = Depends(get_db)
):
    """Upload a file."""
    storage_service = StorageService(db)
    
    # Read file content
    file_content = await file.read()
    
    # Validate file size
    if not storage_service.validate_file_size(len(file_content)):
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {storage_service.max_file_size} bytes"
        )
    
    # Save file
    result = storage_service.save_file(
        file_content=file_content,
        original_filename=file.filename,
        file_type=file.content_type,
        entity_type=entity_type,
        entity_id=entity_id
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result

@router.delete("/{file_id}", response_model=FileResponse)
def delete_file(
    file_id: int,
    db: Session = Depends(get_db)
):
    """Delete a file."""
    storage_service = StorageService(db)
    result = storage_service.delete_file(file_id)
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result

@router.get("/{file_id}", response_model=FileResponse)
def get_file_info(
    file_id: int,
    db: Session = Depends(get_db)
):
    """Get file information."""
    storage_service = StorageService(db)
    result = storage_service.get_file_info(file_id)
    
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    
    return result

@router.get("/entity/{entity_type}/{entity_id}", response_model=FileListResponse)
def get_entity_files(
    entity_type: str,
    entity_id: int,
    db: Session = Depends(get_db)
):
    """Get all files associated with an entity."""
    storage_service = StorageService(db)
    result = storage_service.get_entity_files(entity_type, entity_id)
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    
    return result 