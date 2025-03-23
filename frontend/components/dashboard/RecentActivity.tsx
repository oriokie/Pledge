'use client';

import { Fragment } from 'react';
import { Menu, Transition } from '@headlessui/react';
import {
  CurrencyDollarIcon,
  UserPlusIcon,
  UserGroupIcon,
  FolderPlusIcon,
} from '@heroicons/react/24/outline';
import { formatDate } from '@/lib/utils';
import { cn } from '@/lib/utils';

interface Activity {
  id: string;
  type: 'contribution' | 'member' | 'group' | 'project';
  title: string;
  description: string;
  timestamp: string;
  status?: 'completed' | 'pending' | 'failed';
}

interface RecentActivityProps {
  activities: Activity[];
  className?: string;
}

const activityIcons = {
  contribution: CurrencyDollarIcon,
  member: UserPlusIcon,
  group: UserGroupIcon,
  project: FolderPlusIcon,
};

const statusColors = {
  completed: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  failed: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
};

export default function RecentActivity({
  activities,
  className,
}: RecentActivityProps) {
  return (
    <div className={className}>
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white">
          Recent Activity
        </h3>
        <Menu as="div" className="relative">
          <Menu.Button className="rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 dark:hover:bg-gray-700">
            <span className="sr-only">Open menu</span>
            <svg
              className="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"
              />
            </svg>
          </Menu.Button>
          <Transition
            as={Fragment}
            enter="transition ease-out duration-100"
            enterFrom="transform opacity-0 scale-95"
            enterTo="transform opacity-100 scale-100"
            leave="transition ease-in duration-75"
            leaveFrom="transform opacity-100 scale-100"
            leaveTo="transform opacity-0 scale-95"
          >
            <Menu.Items className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none dark:bg-gray-800">
              <Menu.Item>
                {({ active }) => (
                  <button
                    className={cn(
                      'block w-full px-4 py-2 text-left text-sm',
                      active
                        ? 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-white'
                        : 'text-gray-700 dark:text-gray-300'
                    )}
                  >
                    View all
                  </button>
                )}
              </Menu.Item>
              <Menu.Item>
                {({ active }) => (
                  <button
                    className={cn(
                      'block w-full px-4 py-2 text-left text-sm',
                      active
                        ? 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-white'
                        : 'text-gray-700 dark:text-gray-300'
                    )}
                  >
                    Filter by type
                  </button>
                )}
              </Menu.Item>
            </Menu.Items>
          </Transition>
        </Menu>
      </div>

      <div className="mt-4 flow-root">
        <ul
          role="list"
          className="-my-5 divide-y divide-gray-200 dark:divide-gray-700"
        >
          {activities.map((activity) => {
            const Icon = activityIcons[activity.type];
            return (
              <li key={activity.id} className="py-4">
                <div className="flex items-center space-x-4">
                  <div className="flex-shrink-0">
                    <div className="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center dark:bg-indigo-900">
                      <Icon className="h-5 w-5 text-indigo-600 dark:text-indigo-300" />
                    </div>
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-medium text-gray-900 dark:text-white">
                      {activity.title}
                    </p>
                    <p className="truncate text-sm text-gray-500 dark:text-gray-400">
                      {activity.description}
                    </p>
                  </div>
                  <div className="flex items-center space-x-4">
                    {activity.status && (
                      <span
                        className={cn(
                          'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
                          statusColors[activity.status]
                        )}
                      >
                        {activity.status}
                      </span>
                    )}
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      {formatDate(activity.timestamp)}
                    </span>
                  </div>
                </div>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
} 