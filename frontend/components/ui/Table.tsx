'use client';

import { forwardRef } from 'react';
import { cn } from '@/lib/utils';

interface TableProps extends React.HTMLAttributes<HTMLTableElement> {
  variant?: 'default' | 'bordered' | 'striped';
}

const variantClasses = {
  default: '',
  bordered: 'border-collapse border border-gray-200 dark:border-gray-700',
  striped: 'divide-y divide-gray-200 dark:divide-gray-700',
};

const Table = forwardRef<HTMLTableElement, TableProps>(
  ({ className, variant = 'default', ...props }, ref) => {
    return (
      <div className="relative w-full overflow-auto">
        <table
          ref={ref}
          className={cn('w-full caption-bottom text-sm', variantClasses[variant], className)}
          {...props}
        />
      </div>
    );
  }
);

Table.displayName = 'Table';

interface TableHeaderProps extends React.HTMLAttributes<HTMLTableSectionElement> {}

export function TableHeader({
  className,
  ...props
}: TableHeaderProps) {
  return (
    <thead
      className={cn('[&_tr]:border-b [&_tr]:border-gray-200 dark:[&_tr]:border-gray-700', className)}
      {...props}
    />
  );
}

interface TableBodyProps extends React.HTMLAttributes<HTMLTableSectionElement> {}

export function TableBody({
  className,
  ...props
}: TableBodyProps) {
  return (
    <tbody
      className={cn('[&_tr:last-child]:border-0', className)}
      {...props}
    />
  );
}

interface TableFooterProps extends React.HTMLAttributes<HTMLTableSectionElement> {}

export function TableFooter({
  className,
  ...props
}: TableFooterProps) {
  return (
    <tfoot
      className={cn('bg-gray-100 dark:bg-gray-800 font-medium', className)}
      {...props}
    />
  );
}

interface TableRowProps extends React.HTMLAttributes<HTMLTableRowElement> {
  isSelected?: boolean;
}

export function TableRow({
  className,
  isSelected,
  ...props
}: TableRowProps) {
  return (
    <tr
      className={cn(
        'border-b border-gray-200 dark:border-gray-700 transition-colors hover:bg-gray-50 dark:hover:bg-gray-800/50',
        isSelected && 'bg-gray-50 dark:bg-gray-800/50',
        className
      )}
      {...props}
    />
  );
}

interface TableHeadProps extends React.ThHTMLAttributes<HTMLTableCellElement> {
  sortable?: boolean;
  sortDirection?: 'asc' | 'desc';
}

export function TableHead({
  className,
  sortable,
  sortDirection,
  children,
  ...props
}: TableHeadProps) {
  return (
    <th
      className={cn(
        'h-12 px-4 text-left align-middle font-medium text-gray-500 dark:text-gray-400 [&:has([role=checkbox])]:pr-0',
        sortable && 'cursor-pointer select-none',
        className
      )}
      {...props}
    >
      <div className="flex items-center gap-2">
        {children}
        {sortable && (
          <span className="inline-flex">
            {sortDirection === 'asc' ? (
              <svg
                className="h-4 w-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 15l7-7 7 7"
                />
              </svg>
            ) : sortDirection === 'desc' ? (
              <svg
                className="h-4 w-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            ) : null}
          </span>
        )}
      </div>
    </th>
  );
}

interface TableCellProps extends React.TdHTMLAttributes<HTMLTableCellElement> {}

export function TableCell({
  className,
  ...props
}: TableCellProps) {
  return (
    <td
      className={cn('p-4 align-middle [&:has([role=checkbox])]:pr-0', className)}
      {...props}
    />
  );
}

interface TableCaptionProps extends React.HTMLAttributes<HTMLTableCaptionElement> {}

export function TableCaption({
  className,
  ...props
}: TableCaptionProps) {
  return (
    <caption
      className={cn('mt-4 text-sm text-gray-500 dark:text-gray-400', className)}
      {...props}
    />
  );
}

export default Table; 