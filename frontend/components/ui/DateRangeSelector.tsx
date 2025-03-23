'use client';

import { useState } from 'react';
import { Select } from '@/components/ui/Form';
import { startOfMonth, subMonths, format } from 'date-fns';

interface DateRangeOption {
  label: string;
  value: string;
  startDate: Date;
  endDate: Date;
}

interface DateRangeSelectorProps {
  onChange: (startDate: Date, endDate: Date) => void;
  className?: string;
}

export function DateRangeSelector({ onChange, className }: DateRangeSelectorProps) {
  const today = new Date();
  const ranges: DateRangeOption[] = [
    {
      label: 'Last 7 days',
      value: '7d',
      startDate: new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000),
      endDate: today,
    },
    {
      label: 'Last 30 days',
      value: '30d',
      startDate: new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000),
      endDate: today,
    },
    {
      label: 'This month',
      value: 'this_month',
      startDate: startOfMonth(today),
      endDate: today,
    },
    {
      label: 'Last 3 months',
      value: '3m',
      startDate: subMonths(today, 3),
      endDate: today,
    },
    {
      label: 'Last 6 months',
      value: '6m',
      startDate: subMonths(today, 6),
      endDate: today,
    },
    {
      label: 'Year to date',
      value: 'ytd',
      startDate: new Date(today.getFullYear(), 0, 1),
      endDate: today,
    },
  ];

  const [selectedRange, setSelectedRange] = useState('30d');

  const handleRangeChange = (value: string) => {
    const range = ranges.find((r) => r.value === value);
    if (range) {
      setSelectedRange(value);
      onChange(range.startDate, range.endDate);
    }
  };

  return (
    <div className={className}>
      <Select
        value={selectedRange}
        onChange={(e: React.ChangeEvent<HTMLSelectElement>) => handleRangeChange(e.target.value)}
        className="w-40"
      >
        {ranges.map((range) => (
          <option key={range.value} value={range.value}>
            {range.label}
          </option>
        ))}
      </Select>
    </div>
  );
} 