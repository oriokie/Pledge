'use client';

import { useState, useCallback } from 'react';
import { MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline';
import { Input } from './Form';
import { Button } from './Button';
import { cn } from '@/lib/utils';

export interface FilterOption {
  label: string;
  value: string;
}

export interface SearchFilterProps {
  onSearch: (query: string) => void;
  onFilterChange: (filters: Record<string, string[]>) => void;
  searchPlaceholder?: string;
  filters: {
    label: string;
    key: string;
    options: FilterOption[];
  }[];
  className?: string;
}

export function SearchFilter({
  onSearch,
  onFilterChange,
  searchPlaceholder = 'Search...',
  filters,
  className,
}: SearchFilterProps) {
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilters, setSelectedFilters] = useState<Record<string, string[]>>({});

  const handleSearch = useCallback(
    (value: string) => {
      setSearchQuery(value);
      onSearch(value);
    },
    [onSearch]
  );

  const handleFilterChange = useCallback(
    (key: string, values: string[]) => {
      const newFilters = { ...selectedFilters, [key]: values };
      setSelectedFilters(newFilters);
      onFilterChange(newFilters);
    },
    [selectedFilters, onFilterChange]
  );

  return (
    <div className={cn('space-y-4', className)}>
      <div className="flex items-center space-x-4">
        <div className="relative flex-1">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
          <Input
            type="text"
            placeholder={searchPlaceholder}
            value={searchQuery}
            onChange={(e) => handleSearch(e.target.value)}
            className="pl-10"
          />
        </div>
        <Button
          variant="outline"
          onClick={() => setIsFilterOpen(!isFilterOpen)}
          className="flex items-center space-x-2"
        >
          <FunnelIcon className="h-5 w-5" />
          <span>Filters</span>
        </Button>
      </div>

      {isFilterOpen && (
        <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm dark:border-gray-700 dark:bg-gray-800">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {filters.map((filter) => (
              <div key={filter.key} className="space-y-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
                  {filter.label}
                </label>
                <select
                  multiple
                  value={selectedFilters[filter.key] || []}
                  onChange={(e) => {
                    const values = Array.from(e.target.selectedOptions, (option) => option.value);
                    handleFilterChange(filter.key, values);
                  }}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white sm:text-sm"
                >
                  {filter.options.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
} 