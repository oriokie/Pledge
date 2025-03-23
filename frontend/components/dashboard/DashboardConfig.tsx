'use client';

import { useState } from 'react';
import { Card, Title } from '@tremor/react';
import { Button } from '@/components/ui/Button';
import { Select } from '@/components/ui/Form';
import {
  Cog6ToothIcon,
  XMarkIcon,
  ArrowsUpDownIcon,
} from '@heroicons/react/24/outline';

export interface WidgetConfig {
  id: string;
  name: string;
  enabled: boolean;
  position: number;
  size: 'small' | 'medium' | 'large';
}

export interface FilterConfig {
  groups: string[];
  types: string[];
  categories: string[];
}

interface DashboardConfigProps {
  widgets: WidgetConfig[];
  filters: FilterConfig;
  onWidgetChange: (widgets: WidgetConfig[]) => void;
  onFilterChange: (filters: FilterConfig) => void;
  groups: Array<{ id: string; name: string }>;
}

export function DashboardConfig({
  widgets: initialWidgets,
  filters: initialFilters,
  onWidgetChange,
  onFilterChange,
  groups,
}: DashboardConfigProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [widgets, setWidgets] = useState(initialWidgets);
  const [filters, setFilters] = useState(initialFilters);

  const handleWidgetToggle = (widgetId: string) => {
    const updatedWidgets = widgets.map((widget) =>
      widget.id === widgetId
        ? { ...widget, enabled: !widget.enabled }
        : widget
    );
    setWidgets(updatedWidgets);
    onWidgetChange(updatedWidgets);
  };

  const handleWidgetSizeChange = (widgetId: string, size: WidgetConfig['size']) => {
    const updatedWidgets = widgets.map((widget) =>
      widget.id === widgetId ? { ...widget, size } : widget
    );
    setWidgets(updatedWidgets);
    onWidgetChange(updatedWidgets);
  };

  const handleWidgetMove = (widgetId: string, direction: 'up' | 'down') => {
    const index = widgets.findIndex((w) => w.id === widgetId);
    if (
      (direction === 'up' && index === 0) ||
      (direction === 'down' && index === widgets.length - 1)
    ) {
      return;
    }

    const newIndex = direction === 'up' ? index - 1 : index + 1;
    const updatedWidgets = [...widgets];
    [updatedWidgets[index], updatedWidgets[newIndex]] = [
      updatedWidgets[newIndex],
      updatedWidgets[index],
    ];

    updatedWidgets.forEach((widget, i) => {
      widget.position = i;
    });

    setWidgets(updatedWidgets);
    onWidgetChange(updatedWidgets);
  };

  const handleFilterChange = (
    type: keyof FilterConfig,
    values: string[]
  ) => {
    const updatedFilters = { ...filters, [type]: values };
    setFilters(updatedFilters);
    onFilterChange(updatedFilters);
  };

  if (!isOpen) {
    return (
      <Button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-4 right-4 rounded-full p-3"
      >
        <Cog6ToothIcon className="h-6 w-6" />
      </Button>
    );
  }

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-80 bg-white p-6 shadow-lg dark:bg-gray-900">
      <div className="flex items-center justify-between">
        <Title>Dashboard Settings</Title>
        <button
          onClick={() => setIsOpen(false)}
          className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        >
          <XMarkIcon className="h-6 w-6" />
        </button>
      </div>

      <div className="mt-6">
        <h3 className="text-sm font-medium text-gray-900 dark:text-white">
          Widgets
        </h3>
        <div className="mt-4 space-y-4">
          {widgets.map((widget) => (
            <div
              key={widget.id}
              className="flex items-center justify-between space-x-4"
            >
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={widget.enabled}
                  onChange={() => handleWidgetToggle(widget.id)}
                  className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                />
                <span className="ml-2 text-sm text-gray-900 dark:text-white">
                  {widget.name}
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <Select
                  value={widget.size}
                  onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
                    handleWidgetSizeChange(widget.id, e.target.value as WidgetConfig['size'])
                  }
                  className="w-24 text-sm"
                >
                  <option value="small">Small</option>
                  <option value="medium">Medium</option>
                  <option value="large">Large</option>
                </Select>
                <button
                  onClick={() => handleWidgetMove(widget.id, 'up')}
                  className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                >
                  <ArrowsUpDownIcon className="h-4 w-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-8">
        <h3 className="text-sm font-medium text-gray-900 dark:text-white">
          Filters
        </h3>
        <div className="mt-4 space-y-4">
          <div>
            <label className="text-sm text-gray-700 dark:text-gray-300">
              Groups
            </label>
            <Select
              multiple
              value={filters.groups}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
                handleFilterChange(
                  'groups',
                  Array.from(e.target.selectedOptions, (option: HTMLOptionElement) => option.value)
                )
              }
              className="mt-1"
            >
              {groups.map((group) => (
                <option key={group.id} value={group.id}>
                  {group.name}
                </option>
              ))}
            </Select>
          </div>

          <div>
            <label className="text-sm text-gray-700 dark:text-gray-300">
              Contribution Types
            </label>
            <Select
              multiple
              value={filters.types}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
                handleFilterChange(
                  'types',
                  Array.from(e.target.selectedOptions, (option: HTMLOptionElement) => option.value)
                )
              }
              className="mt-1"
            >
              <option value="tithe">Tithe</option>
              <option value="offering">Offering</option>
              <option value="special">Special</option>
              <option value="project">Project</option>
            </Select>
          </div>

          <div>
            <label className="text-sm text-gray-700 dark:text-gray-300">
              Project Categories
            </label>
            <Select
              multiple
              value={filters.categories}
              onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
                handleFilterChange(
                  'categories',
                  Array.from(e.target.selectedOptions, (option: HTMLOptionElement) => option.value)
                )
              }
              className="mt-1"
            >
              <option value="building">Building</option>
              <option value="missions">Missions</option>
              <option value="outreach">Outreach</option>
              <option value="equipment">Equipment</option>
              <option value="other">Other</option>
            </Select>
          </div>
        </div>
      </div>
    </div>
  );
} 