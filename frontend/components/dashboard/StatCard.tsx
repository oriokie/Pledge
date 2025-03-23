'use client';

import { ElementType } from 'react';
import { cn } from '@/lib/utils';

interface StatCardProps {
  title: string;
  value: number;
  trend: number;
  icon: ElementType;
  isCurrency?: boolean;
  isLoading?: boolean;
  className?: string;
}

export default function StatCard({
  title,
  value,
  trend,
  icon: Icon,
  isCurrency = false,
  isLoading = false,
  className,
}: StatCardProps) {
  const formattedValue = isCurrency
    ? new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(value)
    : value.toLocaleString();

  const isPositive = trend > 0;
  const trendColor = isPositive ? 'text-green-600' : 'text-red-600';
  const trendIcon = isPositive ? '↑' : '↓';

  if (isLoading) {
    return (
      <div
        className={cn(
          'rounded-lg border bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-900',
          className
        )}
      >
        <div className="animate-pulse space-y-4">
          <div className="h-4 w-1/2 rounded bg-gray-200 dark:bg-gray-700" />
          <div className="h-8 w-3/4 rounded bg-gray-200 dark:bg-gray-700" />
          <div className="h-4 w-1/4 rounded bg-gray-200 dark:bg-gray-700" />
        </div>
      </div>
    );
  }

  return (
    <div
      className={cn(
        'rounded-lg border bg-white p-6 shadow-sm dark:border-gray-800 dark:bg-gray-900',
        className
      )}
    >
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">
          {title}
        </h3>
        <Icon className="h-5 w-5 text-gray-400" />
      </div>
      <div className="mt-2">
        <p className="text-3xl font-semibold text-gray-900 dark:text-white">
          {formattedValue}
        </p>
        <p className="mt-2 flex items-center text-sm">
          <span className={cn('font-medium', trendColor)}>
            {trendIcon} {Math.abs(trend)}%
          </span>
          <span className="ml-2 text-gray-500">from last month</span>
        </p>
      </div>
    </div>
  );
} 