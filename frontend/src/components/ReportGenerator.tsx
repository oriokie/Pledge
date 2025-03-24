import { useState } from 'react';
import { reports } from '@/lib/api';
import { Report } from '@/types';

interface ReportGeneratorProps {
  onReportGenerated?: (report: Report) => void;
  onError?: (error: Error) => void;
}

export function ReportGenerator({ onReportGenerated, onError }: ReportGeneratorProps) {
  const [isGenerating, setIsGenerating] = useState(false);
  const [reportType, setReportType] = useState<Report['report_type']>('CONTRIBUTION');
  const [parameters, setParameters] = useState<Record<string, any>>({});

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      const report = await reports.generate(reportType, parameters);
      onReportGenerated?.(report);
    } catch (error) {
      onError?.(error as Error);
    } finally {
      setIsGenerating(false);
    }
  };

  const renderParameters = () => {
    switch (reportType) {
      case 'CONTRIBUTION':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Start Date</label>
              <input
                type="date"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={parameters.startDate || ''}
                onChange={(e) => setParameters({ ...parameters, startDate: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">End Date</label>
              <input
                type="date"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={parameters.endDate || ''}
                onChange={(e) => setParameters({ ...parameters, endDate: e.target.value })}
              />
            </div>
          </div>
        );
      case 'PLEDGE':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Status</label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={parameters.status || ''}
                onChange={(e) => setParameters({ ...parameters, status: e.target.value })}
              >
                <option value="">All</option>
                <option value="PENDING">Pending</option>
                <option value="PAID">Paid</option>
                <option value="CANCELLED">Cancelled</option>
              </select>
            </div>
          </div>
        );
      case 'MEMBER':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Group</label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={parameters.groupId || ''}
                onChange={(e) => setParameters({ ...parameters, groupId: e.target.value })}
              >
                <option value="">All Groups</option>
                {/* Add group options here */}
              </select>
            </div>
          </div>
        );
      case 'GROUP':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Include Members</label>
              <input
                type="checkbox"
                className="mt-1 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                checked={parameters.includeMembers || false}
                onChange={(e) => setParameters({ ...parameters, includeMembers: e.target.checked })}
              />
            </div>
          </div>
        );
      case 'PROJECT':
        return (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Status</label>
              <select
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={parameters.status || ''}
                onChange={(e) => setParameters({ ...parameters, status: e.target.value })}
              >
                <option value="">All</option>
                <option value="PLANNED">Planned</option>
                <option value="IN_PROGRESS">In Progress</option>
                <option value="COMPLETED">Completed</option>
                <option value="CANCELLED">Cancelled</option>
              </select>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700">Report Type</label>
        <select
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          value={reportType}
          onChange={(e) => setReportType(e.target.value as Report['report_type'])}
        >
          <option value="CONTRIBUTION">Contributions</option>
          <option value="PLEDGE">Pledges</option>
          <option value="MEMBER">Members</option>
          <option value="GROUP">Groups</option>
          <option value="PROJECT">Projects</option>
        </select>
      </div>

      {renderParameters()}

      <div>
        <button
          type="button"
          className={`inline-flex justify-center rounded-md border border-transparent bg-blue-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
            isGenerating ? 'opacity-50 cursor-not-allowed' : ''
          }`}
          onClick={handleGenerate}
          disabled={isGenerating}
        >
          {isGenerating ? 'Generating...' : 'Generate Report'}
        </button>
      </div>
    </div>
  );
} 