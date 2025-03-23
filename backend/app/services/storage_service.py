from typing import Dict, Any, Optional
import os
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.file import File
from ..core.config import settings
from ..core.utils import generate_unique_filename

class StorageService:
    def __init__(self, db: Session):
        self.db = db
        self.upload_dir = settings.UPLOAD_DIR
        self.max_file_size = settings.MAX_FILE_SIZE
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS

    def validate_file_type(self, filename: str) -> bool:
        """Validate if file type is allowed."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def validate_file_size(self, file_size: int) -> bool:
        """Validate if file size is within limits."""
        return file_size <= self.max_file_size

    def save_file(
        self,
        file_content: bytes,
        original_filename: str,
        file_type: str,
        entity_type: str,
        entity_id: int
    ) -> Dict[str, Any]:
        """Save file to disk and create database record."""
        try:
            if not self.validate_file_type(original_filename):
                return {
                    "status": "error",
                    "message": f"File type not allowed. Allowed types: {', '.join(self.allowed_extensions)}"
                }

            # Create upload directory if it doesn't exist
            os.makedirs(self.upload_dir, exist_ok=True)

            # Generate unique filename
            filename = generate_unique_filename(original_filename)
            file_path = os.path.join(self.upload_dir, filename)

            # Save file to disk
            with open(file_path, 'wb') as f:
                f.write(file_content)

            # Create file record in database
            file_record = File(
                filename=filename,
                original_filename=original_filename,
                file_type=file_type,
                file_size=len(file_content),
                file_path=file_path,
                entity_type=entity_type,
                entity_id=entity_id
            )
            self.db.add(file_record)
            self.db.commit()

            return {
                "status": "success",
                "file_id": file_record.id,
                "message": "File saved successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_file(self, file_id: int) -> Dict[str, Any]:
        """Delete file from disk and database."""
        try:
            file_record = self.db.query(File).filter(File.id == file_id).first()
            if not file_record:
                return {"status": "error", "message": "File not found"}

            # Delete file from disk
            if os.path.exists(file_record.file_path):
                os.remove(file_record.file_path)

            # Delete record from database
            self.db.delete(file_record)
            self.db.commit()

            return {
                "status": "success",
                "message": "File deleted successfully"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_file_info(self, file_id: int) -> Dict[str, Any]:
        """Get file information."""
        try:
            file_record = self.db.query(File).filter(File.id == file_id).first()
            if not file_record:
                return {"status": "error", "message": "File not found"}

            return {
                "status": "success",
                "file": {
                    "id": file_record.id,
                    "filename": file_record.filename,
                    "original_filename": file_record.original_filename,
                    "file_type": file_record.file_type,
                    "file_size": file_record.file_size,
                    "file_path": file_record.file_path,
                    "entity_type": file_record.entity_type,
                    "entity_id": file_record.entity_id,
                    "created_at": file_record.created_at.isoformat(),
                    "updated_at": file_record.updated_at.isoformat()
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_entity_files(
        self,
        entity_type: str,
        entity_id: int
    ) -> Dict[str, Any]:
        """Get all files associated with an entity."""
        try:
            files = self.db.query(File).filter(
                File.entity_type == entity_type,
                File.entity_id == entity_id
            ).all()

            return {
                "status": "success",
                "files": [
                    {
                        "id": file.id,
                        "filename": file.filename,
                        "original_filename": file.original_filename,
                        "file_type": file.file_type,
                        "file_size": file.file_size,
                        "file_path": file.file_path,
                        "created_at": file.created_at.isoformat(),
                        "updated_at": file.updated_at.isoformat()
                    }
                    for file in files
                ]
            }
        except Exception as e:
            return {"status": "error", "message": str(e)} 