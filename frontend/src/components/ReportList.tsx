import { useState, useEffect } from 'react';
import { Report } from '@/types';
import { reports } from '@/lib/api';

interface ReportListProps {
  onDelete?: (report: Report) => void;
}

export function ReportList({ onDelete }: ReportListProps) {
  const [reportList, setReportList] = useState<Report[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      setIsLoading(true);
      const data = await reports.getAll();
      setReportList(data);
      setError(null);
    } catch (err) {
      setError('Failed to load reports');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (report: Report) => {
    try {
      await reports.delete(report.id);
      onDelete?.(report);
      setReportList(reportList.filter(r => r.id !== report.id));
    } catch (err) {
      setError('Failed to delete report');
    }
  };

  if (isLoading) {
    return <div className="text-center py-4">Loading reports...</div>;
  }

  if (error) {
    return <div className="text-red-500 text-center py-4">{error}</div>;
  }

  if (reportList.length === 0) {
    return <div className="text-gray-500 text-center py-4">No reports generated yet</div>;
  }

  return (
    <div className="space-y-4">
      {reportList.map((report) => (
        <div
          key={report.id}
          className="flex items-center justify-between p-4 bg-white rounded-lg shadow"
        >
          <div className="flex-1">
            <h3 className="text-lg font-medium text-gray-900">{report.title}</h3>
            <div className="mt-1 text-sm text-gray-500">
              <p>{report.description}</p>
              <p>Type: {report.report_type}</p>
              <p>Generated: {new Date(report.created_at).toLocaleDateString()}</p>
              {report.file && (
                <p>
                  File:{' '}
                  <a
                    href={report.file.file_path}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800"
                  >
                    {report.file.name}
                  </a>
                </p>
              )}
            </div>
          </div>
          <div className="ml-4">
            <button
              onClick={() => handleDelete(report)}
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