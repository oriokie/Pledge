import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { files } from '@/lib/api';
import { File } from '@/types';

interface FileUploadProps {
  onUploadSuccess?: (file: File) => void;
  onUploadError?: (error: Error) => void;
  maxSize?: number;
  accept?: Record<string, string[]>;
}

export function FileUpload({
  onUploadSuccess,
  onUploadError,
  maxSize = 5242880, // 5MB
  accept = {
    'application/pdf': ['.pdf'],
    'image/*': ['.png', '.jpg', '.jpeg', '.gif'],
    'application/msword': ['.doc'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    'application/vnd.ms-excel': ['.xls'],
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
  },
}: FileUploadProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      setIsUploading(true);
      setUploadProgress(0);

      try {
        for (const file of acceptedFiles) {
          const uploadedFile = await files.upload(file);
          onUploadSuccess?.(uploadedFile);
          setUploadProgress((prev) => prev + 100 / acceptedFiles.length);
        }
      } catch (error) {
        onUploadError?.(error as Error);
      } finally {
        setIsUploading(false);
        setUploadProgress(0);
      }
    },
    [onUploadSuccess, onUploadError]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxSize,
    accept,
    multiple: true,
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          isDragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
      >
        <input {...getInputProps()} />
        {isUploading ? (
          <div className="space-y-4">
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-600">Uploading... {Math.round(uploadProgress)}%</p>
          </div>
        ) : (
          <div className="space-y-2">
            <div className="text-gray-600">
              {isDragActive ? (
                <p>Drop the files here...</p>
              ) : (
                <p>Drag and drop files here, or click to select files</p>
              )}
            </div>
            <p className="text-sm text-gray-500">
              Supported formats: PDF, Images, Word, Excel
              <br />
              Max size: {maxSize / 1024 / 1024}MB
            </p>
          </div>
        )}
      </div>
    </div>
  );
} 