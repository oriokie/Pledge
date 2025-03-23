from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FileBase(BaseModel):
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    file_path: str
    entity_type: str
    entity_id: int

class FileCreate(FileBase):
    pass

class FileUpdate(BaseModel):
    filename: Optional[str] = None
    original_filename: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    file_path: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None

class FileInDB(FileBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class FileResponse(BaseModel):
    status: str
    file: Optional[FileInDB] = None
    message: Optional[str] = None

class FileListResponse(BaseModel):
    status: str
    files: Optional[list[FileInDB]] = None
    message: Optional[str] = None 