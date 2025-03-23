'use client';

import { useState, useEffect } from 'react';
import { DataGrid } from '@/components/ui/DataGrid';
import { Button } from '@/components/ui/Button';
import { PlusIcon } from '@heroicons/react/24/outline';

interface Group {
  id: string;
  name: string;
  description: string;
  leader: string;
  memberCount: number;
  meetingDay: string;
  meetingTime: string;
  status: 'active' | 'inactive';
}

export default function GroupsPage() {
  const [groups, setGroups] = useState<Group[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // TODO: Replace with actual API call
    const fetchGroups = async () => {
      try {
        // Mock data for now
        const mockGroups: Group[] = [
          {
            id: '1',
            name: 'Prayer Warriors',
            description: 'A group dedicated to intercessory prayer',
            leader: 'John Doe',
            memberCount: 15,
            meetingDay: 'Monday',
            meetingTime: '18:00',
            status: 'active',
          },
          {
            id: '2',
            name: 'Youth Ministry',
            description: 'Group for young adults and teenagers',
            leader: 'Jane Smith',
            memberCount: 25,
            meetingDay: 'Saturday',
            meetingTime: '16:00',
            status: 'active',
          },
          {
            id: '3',
            name: 'Choir',
            description: 'Church choir and worship team',
            leader: 'Bob Johnson',
            memberCount: 20,
            meetingDay: 'Wednesday',
            meetingTime: '19:00',
            status: 'active',
          },
        ];
        setGroups(mockGroups);
      } catch (error) {
        console.error('Error fetching groups:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchGroups();
  }, []);

  const columns = [
    {
      key: 'name',
      header: 'Group Name',
      sortable: true,
      filterable: true,
    },
    {
      key: 'leader',
      header: 'Leader',
      sortable: true,
      filterable: true,
    },
    {
      key: 'memberCount',
      header: 'Members',
      sortable: true,
    },
    {
      key: 'meetingDay',
      header: 'Meeting Day',
      sortable: true,
      filterable: true,
    },
    {
      key: 'meetingTime',
      header: 'Meeting Time',
      sortable: true,
    },
    {
      key: 'status',
      header: 'Status',
      sortable: true,
      filterable: true,
      render: (group: Group) => (
        <span
          className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
            group.status === 'active'
              ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
              : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
          }`}
        >
          {group.status}
        </span>
      ),
    },
    {
      key: 'actions',
      header: 'Actions',
      render: (group: Group) => (
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={() => handleEdit(group)}>
            Edit
          </Button>
          <Button
            variant="destructive"
            size="sm"
            onClick={() => handleDelete(group)}
          >
            Delete
          </Button>
        </div>
      ),
    },
  ];

  const handleEdit = (group: Group) => {
    // TODO: Implement edit functionality
    console.log('Edit group:', group);
  };

  const handleDelete = (group: Group) => {
    // TODO: Implement delete functionality
    console.log('Delete group:', group);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Groups
          </h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Manage church groups and their members
          </p>
        </div>
        <Button>
          <PlusIcon className="mr-2 h-4 w-4" />
          New Group
        </Button>
      </div>

      <div className="rounded-lg border border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800">
        <DataGrid
          columns={columns}
          data={groups}
          pageSize={10}
          showSearch
          showFilters
          isLoading={isLoading}
        />
      </div>
    </div>
  );
} 