'use client';

import { useState, useEffect } from 'react';
import { DataGrid } from '@/components/ui/DataGrid';
import { Button } from '@/components/ui/Button';
import { PlusIcon } from '@heroicons/react/24/outline';
import { formatCurrency, formatDate } from '@/lib/utils';

interface Project {
  id: string;
  name: string;
  description: string;
  target: number;
  raised: number;
  startDate: string;
  endDate: string;
  status: 'active' | 'completed' | 'cancelled';
  progress: number;
}

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // TODO: Replace with actual API call
    const fetchProjects = async () => {
      try {
        // Mock data for now
        const mockProjects: Project[] = [
          {
            id: '1',
            name: 'Church Building Fund',
            description: 'Fundraising for the new church building construction',
            target: 500000,
            raised: 350000,
            startDate: '2024-01-01',
            endDate: '2024-12-31',
            status: 'active',
            progress: 70,
          },
          {
            id: '2',
            name: 'Mission Trip',
            description: 'Annual mission trip to remote areas',
            target: 25000,
            raised: 25000,
            startDate: '2024-03-01',
            endDate: '2024-03-31',
            status: 'completed',
            progress: 100,
          },
          {
            id: '3',
            name: 'Youth Center',
            description: 'Renovation of the youth center',
            target: 75000,
            raised: 15000,
            startDate: '2024-04-01',
            endDate: '2024-06-30',
            status: 'active',
            progress: 20,
          },
        ];
        setProjects(mockProjects);
      } catch (error) {
        console.error('Error fetching projects:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProjects();
  }, []);

  const columns = [
    {
      key: 'name',
      header: 'Project Name',
      sortable: true,
      filterable: true,
    },
    {
      key: 'target',
      header: 'Target',
      sortable: true,
      render: (project: Project) => formatCurrency(project.target),
    },
    {
      key: 'raised',
      header: 'Raised',
      sortable: true,
      render: (project: Project) => formatCurrency(project.raised),
    },
    {
      key: 'progress',
      header: 'Progress',
      sortable: true,
      render: (project: Project) => (
        <div className="w-full">
          <div className="flex items-center">
            <div className="flex-1">
              <div className="h-2 w-full bg-gray-200 rounded-full dark:bg-gray-700">
                <div
                  className="h-2 rounded-full bg-primary"
                  style={{ width: `${project.progress}%` }}
                />
              </div>
            </div>
            <span className="ml-2 text-sm text-gray-600 dark:text-gray-400">
              {project.progress}%
            </span>
          </div>
        </div>
      ),
    },
    {
      key: 'startDate',
      header: 'Start Date',
      sortable: true,
      render: (project: Project) => formatDate(project.startDate),
    },
    {
      key: 'endDate',
      header: 'End Date',
      sortable: true,
      render: (project: Project) => formatDate(project.endDate),
    },
    {
      key: 'status',
      header: 'Status',
      sortable: true,
      filterable: true,
      render: (project: Project) => (
        <span
          className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
            project.status === 'active'
              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
              : project.status === 'completed'
              ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
              : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
          }`}
        >
          {project.status}
        </span>
      ),
    },
    {
      key: 'actions',
      header: 'Actions',
      render: (project: Project) => (
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={() => handleEdit(project)}>
            Edit
          </Button>
          <Button
            variant="destructive"
            size="sm"
            onClick={() => handleDelete(project)}
          >
            Delete
          </Button>
        </div>
      ),
    },
  ];

  const handleEdit = (project: Project) => {
    // TODO: Implement edit functionality
    console.log('Edit project:', project);
  };

  const handleDelete = (project: Project) => {
    // TODO: Implement delete functionality
    console.log('Delete project:', project);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Projects
          </h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Manage church projects and track their progress
          </p>
        </div>
        <Button>
          <PlusIcon className="mr-2 h-4 w-4" />
          New Project
        </Button>
      </div>

      <div className="rounded-lg border border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800">
        <DataGrid
          columns={columns}
          data={projects}
          pageSize={10}
          showSearch
          showFilters
          isLoading={isLoading}
        />
      </div>
    </div>
  );
} 