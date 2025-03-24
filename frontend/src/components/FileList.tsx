import { useState, useEffect } from 'react';
import { File } from '@/types';
import { files } from '@/lib/api';

interface FileListProps {
  onDelete?: (file: File) => void;
}

export function FileList({ onDelete }: FileListProps) {
  const [fileList, setFileList] = useState<File[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    try {
      setIsLoading(true);
      const data = await files.getAll();
      setFileList(data);
      setError(null);
    } catch (err) {
      setError('Failed to load files');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (file: File) => {
    try {
      await files.delete(file.id);
      onDelete?.(file);
      setFileList(fileList.filter(f => f.id !== file.id));
    } catch (err) {
      setError('Failed to delete file');
    }
  };

  if (isLoading) {
    return <div className="text-center py-4">Loading files...</div>;
  }

  if (error) {
    return <div className="text-red-500 text-center py-4">{error}</div>;
  }

  if (fileList.length === 0) {
    return <div className="text-gray-500 text-center py-4">No files uploaded yet</div>;
  }

  return (
    <div className="space-y-4">
      {fileList.map((file) => (
        <div
          key={file.id}
          className="flex items-center justify-between p-4 bg-white rounded-lg shadow"
        >
          <div className="flex-1">
            <h3 className="text-lg font-medium text-gray-900">{file.name}</h3>
            <div className="mt-1 text-sm text-gray-500">
              <p>Type: {file.file_type}</p>
              <p>Size: {(file.file_size / 1024).toFixed(2)} KB</p>
              <p>Uploaded: {new Date(file.created_at).toLocaleDateString()}</p>
            </div>
          </div>
          <div className="ml-4">
            <button
              onClick={() => handleDelete(file)}
              className="text-red-600 hover:text-red-800"
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
} 