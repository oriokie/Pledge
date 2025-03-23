'use client';

import { forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'bordered' | 'elevated';
  padding?: 'none' | 'sm' | 'md' | 'lg';
}

const variantClasses = {
  default: 'bg-white dark:bg-gray-800',
  bordered: 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700',
  elevated: 'bg-white dark:bg-gray-800 shadow-lg',
};

const paddingClasses = {
  none: '',
  sm: 'p-4',
  md: 'p-6',
  lg: 'p-8',
};

const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = 'default', padding = 'md', ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'rounded-lg',
          variantClasses[variant],
          paddingClasses[padding],
          className
        )}
        {...props}
      />
    );
  }
);

Card.displayName = 'Card';

interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  subtitle?: string;
}

export function CardHeader({
  className,
  title,
  subtitle,
  children,
  ...props
}: CardHeaderProps) {
  return (
    <div
      className={cn('flex flex-col space-y-1.5', className)}
      {...props}
    >
      {title && (
        <h3 className="text-lg font-semibold leading-none tracking-tight text-gray-900 dark:text-white">
          {title}
        </h3>
      )}
      {subtitle && (
        <p className="text-sm text-gray-500 dark:text-gray-400">
          {subtitle}
        </p>
      )}
      {children}
    </div>
  );
}

interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {}

export function CardContent({
  className,
  ...props
}: CardContentProps) {
  return (
    <div
      className={cn('pt-0', className)}
      {...props}
    />
  );
}

interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {}

export function CardFooter({
  className,
  ...props
}: CardFooterProps) {
  return (
    <div
      className={cn('flex items-center pt-4', className)}
      {...props}
    />
  );
}

interface AdvancedFilters {
  contributionTypes: string[];
  projectCategories: string[];
  memberGroups: string[];
  dateRanges: {
    custom: DateRange;
    presets: {
      lastWeek: DateRange;
      lastMonth: DateRange;
      lastQuarter: DateRange;
      lastYear: DateRange;
    };
  };
}

interface AdvancedAnalytics {
  contributionPredictions: {
    nextMonth: number;
    confidence: number;
  };
  memberRetention: {
    rate: number;
    trend: number;
  };
  projectSuccess: {
    rate: number;
    factors: string[];
  };
}

interface ExportOptions {
  format: 'csv' | 'excel' | 'pdf';
  dateRange: DateRange;
  dataType: 'contributions' | 'members' | 'projects' | 'events';
  includeCharts: boolean;
}

interface DashboardLayout {
  id: string;
  name: string;
  widgets: {
    id: string;
    type: string;
    position: { x: number; y: number };
    size: { width: number; height: number };
  }[];
}

interface BatchOperation {
  type: 'create' | 'update' | 'delete';
  entity: 'contribution' | 'member' | 'project' | 'event';
  data: any[];
}

export default Card; 