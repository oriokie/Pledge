'use client';

import { useState } from 'react';
import { File, Report } from '@/types';
import { FileUpload } from '@/components/FileUpload';
import { FileList } from '@/components/FileList';
import { ReportGenerator } from '@/components/ReportGenerator';
import { ReportList } from '@/components/ReportList';

export default function ReportsPage() {
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [reportError, setReportError] = useState<string | null>(null);

  const handleUploadSuccess = (file: File) => {
    setUploadError(null);
  };

  const handleUploadError = (error: Error) => {
    setUploadError(error.message);
  };

  const handleReportGenerated = (report: Report) => {
    setReportError(null);
  };

  const handleReportError = (error: Error) => {
    setReportError(error.message);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Files & Reports</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <h2 className="text-2xl font-semibold mb-4">Upload Files</h2>
          <div className="space-y-4">
            <FileUpload
              onUploadSuccess={handleUploadSuccess}
              onUploadError={handleUploadError}
            />
            {uploadError && (
              <div className="text-red-500">{uploadError}</div>
            )}
            <div className="mt-8">
              <h3 className="text-xl font-semibold mb-4">Uploaded Files</h3>
              <FileList />
            </div>
          </div>
        </div>

        <div>
          <h2 className="text-2xl font-semibold mb-4">Generate Reports</h2>
          <div className="space-y-4">
            <ReportGenerator
              onReportGenerated={handleReportGenerated}
              onError={handleReportError}
            />
            {reportError && (
              <div className="text-red-500">{reportError}</div>
            )}
            <div className="mt-8">
              <h3 className="text-xl font-semibold mb-4">Generated Reports</h3>
              <ReportList />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 