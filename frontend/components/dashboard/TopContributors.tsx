'use client';

import { Card, Title } from '@tremor/react';
import { UserIcon } from '@heroicons/react/24/outline';

interface Contributor {
  id: string;
  name: string;
  amount: number;
  contributions: number;
  trend: number;
}

interface TopContributorsProps {
  data?: Contributor[];
  isLoading?: boolean;
}

export function TopContributors({ data, isLoading }: TopContributorsProps) {
  // Mock data if none provided
  const contributors = data || [
    {
      id: '1',
      name: 'John Doe',
      amount: 5000,
      contributions: 12,
      trend: 15,
    },
    {
      id: '2',
      name: 'Jane Smith',
      amount: 4200,
      contributions: 8,
      trend: 5,
    },
    {
      id: '3',
      name: 'Robert Johnson',
      amount: 3800,
      contributions: 10,
      trend: -2,
    },
    {
      id: '4',
      name: 'Sarah Williams',
      amount: 3500,
      contributions: 6,
      trend: 8,
    },
    {
      id: '5',
      name: 'Michael Brown',
      amount: 3200,
      contributions: 7,
      trend: 3,
    },
  ];

  if (isLoading) {
    return (
      <Card className="mt-4">
        <Title>Top Contributors</Title>
        <div className="mt-4 space-y-4">
          {[...Array(5)].map((_, i) => (
            <div
              key={i}
              className="flex animate-pulse items-center space-x-4 rounded-lg border p-4"
            >
              <div className="h-10 w-10 rounded-full bg-gray-200 dark:bg-gray-700" />
              <div className="flex-1 space-y-2">
                <div className="h-4 w-1/3 rounded bg-gray-200 dark:bg-gray-700" />
                <div className="h-3 w-1/4 rounded bg-gray-200 dark:bg-gray-700" />
              </div>
              <div className="h-4 w-20 rounded bg-gray-200 dark:bg-gray-700" />
            </div>
          ))}
        </div>
      </Card>
    );
  }

  return (
    <Card className="mt-4">
      <Title>Top Contributors</Title>
      <div className="mt-4 space-y-4">
        {contributors.map((contributor) => (
          <div
            key={contributor.id}
            className="flex items-center space-x-4 rounded-lg border p-4 hover:bg-gray-50 dark:hover:bg-gray-800"
          >
            <div className="flex-shrink-0">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-indigo-100 dark:bg-indigo-900">
                <UserIcon className="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
              </div>
            </div>
            <div className="min-w-0 flex-1">
              <div className="text-sm font-medium text-gray-900 dark:text-white">
                {contributor.name}
              </div>
              <div className="mt-1 flex items-center text-sm text-gray-500">
                <span>{contributor.contributions} contributions</span>
                <span className="mx-2">•</span>
                <span>
                  {new Intl.NumberFormat('en-US', {
                    style: 'currency',
                    currency: 'USD',
                  }).format(contributor.amount)}
                </span>
              </div>
            </div>
            <div
              className={`flex items-center text-sm font-medium ${
                contributor.trend > 0
                  ? 'text-green-600'
                  : contributor.trend < 0
                  ? 'text-red-600'
                  : 'text-gray-500'
              }`}
            >
              {contributor.trend > 0 ? '↑' : contributor.trend < 0 ? '↓' : ''}
              {Math.abs(contributor.trend)}%
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
} 