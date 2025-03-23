'use client';

import { useState, useMemo } from 'react';
import Table, {
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from './Table';
import Pagination from './Pagination';
import { Input } from './Form';

interface Column<T> {
  key: keyof T | string;
  header: string;
  render?: (item: T) => React.ReactNode;
  sortable?: boolean;
  filterable?: boolean;
}

interface DataGridProps<T> {
  columns: Column<T>[];
  data: T[];
  pageSize?: number;
  showPagination?: boolean;
  showSearch?: boolean;
  showFilters?: boolean;
  className?: string;
}

export default function DataGrid<T extends { id: string | number }>({
  columns,
  data,
  pageSize = 10,
  showPagination = true,
  showSearch = true,
  showFilters = true,
  className,
}: DataGridProps<T>) {
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState<{
    key: keyof T | string;
    direction: 'asc' | 'desc';
  } | null>(null);
  const [filters, setFilters] = useState<Record<string, string>>({});

  // Filter data based on search term and filters
  const filteredData = useMemo(() => {
    return data.filter((item) => {
      const matchesSearch = searchTerm
        ? Object.values(item).some((value) =>
            String(value).toLowerCase().includes(searchTerm.toLowerCase())
          )
        : true;

      const matchesFilters = Object.entries(filters).every(
        ([key, value]) =>
          !value || String(item[key as keyof T]).toLowerCase().includes(value.toLowerCase())
      );

      return matchesSearch && matchesFilters;
    });
  }, [data, searchTerm, filters]);

  // Sort data
  const sortedData = useMemo(() => {
    if (!sortConfig) return filteredData;

    return [...filteredData].sort((a, b) => {
      const aValue = a[sortConfig.key as keyof T];
      const bValue = b[sortConfig.key as keyof T];

      if (aValue === bValue) return 0;
      if (aValue === null) return 1;
      if (bValue === null) return -1;

      const comparison = String(aValue).localeCompare(String(bValue));
      return sortConfig.direction === 'asc' ? comparison : -comparison;
    });
  }, [filteredData, sortConfig]);

  // Paginate data
  const paginatedData = useMemo(() => {
    if (!showPagination) return sortedData;
    const startIndex = (currentPage - 1) * pageSize;
    return sortedData.slice(startIndex, startIndex + pageSize);
  }, [sortedData, currentPage, pageSize, showPagination]);

  const totalPages = Math.ceil(filteredData.length / pageSize);

  const handleSort = (key: keyof T | string) => {
    setSortConfig((current) => {
      if (current?.key === key) {
        return {
          key,
          direction: current.direction === 'asc' ? 'desc' : 'asc',
        };
      }
      return { key, direction: 'asc' };
    });
  };

  const handleFilterChange = (key: string, value: string) => {
    setFilters((current) => ({
      ...current,
      [key]: value,
    }));
  };

  return (
    <div className={className}>
      {showSearch && (
        <div className="mb-4">
          <Input
            type="search"
            placeholder="Search..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="max-w-sm"
          />
        </div>
      )}

      {showFilters && (
        <div className="mb-4 flex gap-4">
          {columns
            .filter((column) => column.filterable)
            .map((column) => (
              <Input
                key={String(column.key)}
                type="text"
                placeholder={`Filter ${column.header}...`}
                value={filters[String(column.key)] || ''}
                onChange={(e) =>
                  handleFilterChange(String(column.key), e.target.value)
                }
                className="max-w-xs"
              />
            ))}
        </div>
      )}

      <Table>
        <TableHeader>
          <TableRow>
            {columns.map((column) => (
              <TableHead
                key={String(column.key)}
                sortable={column.sortable}
                sortDirection={
                  sortConfig?.key === column.key ? sortConfig.direction : undefined
                }
                onClick={() => column.sortable && handleSort(column.key)}
                className={column.sortable ? 'cursor-pointer' : ''}
              >
                {column.header}
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {paginatedData.map((item) => (
            <TableRow key={item.id}>
              {columns.map((column) => (
                <TableCell key={String(column.key)}>
                  {column.render
                    ? column.render(item)
                    : String(item[column.key as keyof T])}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {showPagination && (
        <div className="mt-4">
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
          />
        </div>
      )}
    </div>
  );
} 