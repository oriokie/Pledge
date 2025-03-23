'use client';

import { useState, useRef } from 'react';
import { cn } from '@/lib/utils';
import { CloudArrowUpIcon, XMarkIcon } from '@heroicons/react/24/outline';

interface FileUploadProps {
  label?: string;
  accept?: string;
  maxSize?: number;
  preview?: string;
  onUpload: (file: File) => void;
  className?: string;
}

export function FileUpload({
  label,
  accept,
  maxSize = 5 * 1024 * 1024, // 5MB default
  preview,
  onUpload,
  className,
}: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string>();
  const [previewUrl, setPreviewUrl] = useState(preview);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const validateFile = (file: File): boolean => {
    if (maxSize && file.size > maxSize) {
      setError(`File size must be less than ${maxSize / 1024 / 1024}MB`);
      return false;
    }

    if (accept) {
      const acceptedTypes = accept.split(',').map((type) => type.trim());
      if (!acceptedTypes.some((type) => {
        if (type.startsWith('.')) {
          return file.name.toLowerCase().endsWith(type.toLowerCase());
        }
        return file.type.match(new RegExp(type.replace('*', '.*')));
      })) {
        setError(`File type must be ${accept}`);
        return false;
      }
    }

    return true;
  };

  const handleFile = (file: File) => {
    setError(undefined);

    if (!validateFile(file)) {
      return;
    }

    // Create preview URL for images
    if (file.type.startsWith('image/')) {
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    }

    onUpload(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) {
      handleFile(file);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFile(file);
    }
  };

  const handleRemove = () => {
    setPreviewUrl(undefined);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className={className}>
      {label && (
        <label className="block text-sm font-medium text-gray-900 dark:text-gray-200 mb-2">
          {label}
        </label>
      )}
      <div
        className={cn(
          'relative rounded-lg border-2 border-dashed p-6 transition-colors',
          isDragging
            ? 'border-primary bg-primary/5'
            : 'border-gray-300 dark:border-gray-700',
          className
        )}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept={accept}
          onChange={handleChange}
          className="absolute inset-0 h-full w-full cursor-pointer opacity-0"
        />
        <div className="text-center">
          {previewUrl ? (
            <div className="relative inline-block">
              <img
                src={previewUrl}
                alt="Preview"
                className="max-h-48 rounded-lg object-contain"
              />
              <button
                type="button"
                onClick={handleRemove}
                className="absolute -right-2 -top-2 rounded-full bg-red-500 p-1 text-white hover:bg-red-600"
              >
                <XMarkIcon className="h-4 w-4" />
              </button>
            </div>
          ) : (
            <>
              <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
              <div className="mt-4">
                <span className="text-sm font-medium text-primary">
                  Click to upload
                </span>{' '}
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  or drag and drop
                </span>
              </div>
              <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                {accept
                  ? `${accept.split(',').join(', ')} files up to ${
                      maxSize / 1024 / 1024
                    }MB`
                  : `Files up to ${maxSize / 1024 / 1024}MB`}
              </p>
            </>
          )}
        </div>
        {error && (
          <p className="mt-2 text-sm text-red-600 dark:text-red-500">{error}</p>
        )}
      </div>
    </div>
  );
} 