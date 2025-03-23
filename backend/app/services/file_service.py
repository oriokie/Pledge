from typing import Dict, Any, Optional
import os
from datetime import datetime
from ..core.utils import sanitize_filename
from ..core.config import settings

class FileService:
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        self.allowed_extensions = settings.ALLOWED_FILE_EXTENSIONS
        self.max_file_size = settings.MAX_FILE_SIZE

    def validate_file_type(self, filename: str, allowed_extensions: Optional[list] = None) -> bool:
        """Validate file type."""
        if allowed_extensions is None:
            allowed_extensions = self.allowed_extensions
        return any(filename.lower().endswith(ext) for ext in allowed_extensions)

    def validate_file_size(self, file_size: int, max_size: Optional[int] = None) -> bool:
        """Validate file size."""
        if max_size is None:
            max_size = self.max_file_size
        return file_size <= max_size

    def generate_filename(self, original_filename: str) -> str:
        """Generate a unique filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(original_filename)
        sanitized_name = sanitize_filename(name)
        return f"{sanitized_name}_{timestamp}{ext}"

    def save_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Save file to disk."""
        try:
            if not os.path.exists(self.upload_dir):
                os.makedirs(self.upload_dir)

            file_path = os.path.join(self.upload_dir, filename)
            with open(file_path, "wb") as f:
                f.write(file_content)

            return {
                "status": "success",
                "message": "File saved successfully",
                "file_path": file_path
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_file(self, file_path: str) -> Dict[str, Any]:
        """Delete file from disk."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return {"status": "success", "message": "File deleted successfully"}
            return {"status": "error", "message": "File not found"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get file information."""
        try:
            if not os.path.exists(file_path):
                return {"status": "error", "message": "File not found"}

            stat = os.stat(file_path)
            return {
                "status": "success",
                "size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_ctime),
                "modified_at": datetime.fromtimestamp(stat.st_mtime),
                "file_path": file_path
            }
        except Exception as e:
            return {"status": "error", "message": str(e)} 