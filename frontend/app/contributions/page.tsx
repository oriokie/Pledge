'use client';

import { useState, useEffect } from 'react';
import Layout from '@/components/layout/Layout';
import { DataGrid } from '@/components/ui/DataGrid';
import { Button } from '@/components/ui/Button';
import { CurrencyDollarIcon } from '@heroicons/react/24/outline';
import { formatCurrency, formatDate } from '@/lib/utils';

interface Contribution {
  id: string;
  memberId: string;
  memberName: string;
  amount: number;
  type: 'tithe' | 'offering' | 'project' | 'other';
  project?: string;
  date: string;
  status: 'completed' | 'pending' | 'failed';
  paymentMethod: 'cash' | 'card' | 'bank_transfer' | 'mobile_money';
}

export default function ContributionsPage() {
  const [contributions, setContributions] = useState<Contribution[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // TODO: Replace with actual API call
    const fetchContributions = async () => {
      try {
        // Mock data for now
        const mockContributions: Contribution[] = [
          {
            id: '1',
            memberId: '1',
            memberName: 'John Doe',
            amount: 1000,
            type: 'tithe',
            date: '2024-03-10',
            status: 'completed',
            paymentMethod: 'card',
          },
          // Add more mock data as needed
        ];
        setContributions(mockContributions);
      } catch (error) {
        console.error('Error fetching contributions:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchContributions();
  }, []);

  const columns = [
    {
      key: 'memberName',
      header: 'Member',
      sortable: true,
      filterable: true,
    },
    {
      key: 'amount',
      header: 'Amount',
      sortable: true,
      render: (contribution: Contribution) => formatCurrency(contribution.amount),
    },
    {
      key: 'type',
      header: 'Type',
      sortable: true,
      filterable: true,
      render: (contribution: Contribution) => (
        <span className="capitalize">{contribution.type}</span>
      ),
    },
    {
      key: 'project',
      header: 'Project',
      sortable: true,
      filterable: true,
      render: (contribution: Contribution) =>
        contribution.project || 'Not Applicable',
    },
    {
      key: 'date',
      header: 'Date',
      sortable: true,
      render: (contribution: Contribution) => formatDate(contribution.date),
    },
    {
      key: 'status',
      header: 'Status',
      sortable: true,
      render: (contribution: Contribution) => (
        <span
          className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
            contribution.status === 'completed'
              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
              : contribution.status === 'pending'
              ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
              : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
          }`}
        >
          {contribution.status}
        </span>
      ),
    },
    {
      key: 'paymentMethod',
      header: 'Payment Method',
      sortable: true,
      filterable: true,
      render: (contribution: Contribution) => (
        <span className="capitalize">
          {contribution.paymentMethod.replace('_', ' ')}
        </span>
      ),
    },
    {
      key: 'actions',
      header: 'Actions',
      render: (contribution: Contribution) => (
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={() => handleEdit(contribution)}>
            Edit
          </Button>
          <Button
            variant="destructive"
            size="sm"
            onClick={() => handleDelete(contribution)}
          >
            Delete
          </Button>
        </div>
      ),
    },
  ];

  const handleEdit = (contribution: Contribution) => {
    // TODO: Implement edit functionality
    console.log('Edit contribution:', contribution);
  };

  const handleDelete = (contribution: Contribution) => {
    // TODO: Implement delete functionality
    console.log('Delete contribution:', contribution);
  };

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Contributions
            </h1>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              Manage member contributions and payments
            </p>
          </div>
          <Button>
            <CurrencyDollarIcon className="mr-2 h-4 w-4" />
            New Contribution
          </Button>
        </div>

        <div className="rounded-lg border border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800">
          <DataGrid
            columns={columns}
            data={contributions}
            pageSize={10}
            showSearch
            showFilters
          />
        </div>
      </div>
    </Layout>
  );
} 