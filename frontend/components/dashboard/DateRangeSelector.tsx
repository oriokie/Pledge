'use client';

import { useState } from 'react';
import { format } from 'date-fns';
import { CalendarIcon } from '@heroicons/react/24/outline';
import { Button } from '@/components/ui/Button';
import { cn } from '@/lib/utils';

interface DateRange {
  start: Date;
  end: Date;
}

interface DateRangeSelectorProps {
  onChange: (range: DateRange) => void;
  className?: string;
}

const presets = [
  { label: 'Last 7 days', days: 7 },
  { label: 'Last 30 days', days: 30 },
  { label: 'Last 90 days', days: 90 },
  { label: 'Last year', days: 365 },
];

export function DateRangeSelector({ onChange, className }: DateRangeSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedRange, setSelectedRange] = useState<DateRange>({
    start: new Date(new Date().setDate(new Date().getDate() - 30)),
    end: new Date(),
  });

  const handlePresetSelect = (days: number) => {
    const end = new Date();
    const start = new Date(new Date().setDate(end.getDate() - days));
    const range = { start, end };
    setSelectedRange(range);
    onChange(range);
    setIsOpen(false);
  };

  return (
    <div className={cn('relative', className)}>
      <Button
        variant="outline"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center space-x-2"
      >
        <CalendarIcon className="h-5 w-5" />
        <span>
          {format(selectedRange.start, 'MMM d')} - {format(selectedRange.end, 'MMM d')}
        </span>
      </Button>

      {isOpen && (
        <div className="absolute right-0 top-full z-50 mt-2 w-64 rounded-lg border border-gray-200 bg-white p-4 shadow-lg dark:border-gray-700 dark:bg-gray-800">
          <div className="space-y-2">
            {presets.map((preset) => (
              <button
                key={preset.days}
                onClick={() => handlePresetSelect(preset.days)}
                className="w-full rounded-md px-4 py-2 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                {preset.label}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
} 