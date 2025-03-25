'use client';

import { useAuth } from '@/contexts/AuthContext';
import {
  ArrowUpIcon,
  ArrowDownIcon,
  UserGroupIcon,
  FolderIcon,
  CurrencyDollarIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline';

const stats = [
  {
    name: 'Total Members',
    value: '0',
    change: '+0%',
    changeType: 'increase',
    icon: UserGroupIcon,
  },
  {
    name: 'Active Projects',
    value: '0',
    change: '+0%',
    changeType: 'increase',
    icon: FolderIcon,
  },
  {
    name: 'Total Pledges',
    value: '0',
    change: '+0%',
    changeType: 'increase',
    icon: CurrencyDollarIcon,
  },
  {
    name: 'Completion Rate',
    value: '0%',
    change: '+0%',
    changeType: 'increase',
    icon: ChartBarIcon,
  },
];

const recentActivity = [
  {
    id: 1,
    type: 'pledge',
    description: 'New pledge created',
    amount: 'KES 5,000',
    date: '2 hours ago',
  },
  {
    id: 2,
    type: 'member',
    description: 'New member joined',
    amount: null,
    date: '4 hours ago',
  },
  {
    id: 3,
    type: 'project',
    description: 'Project status updated',
    amount: null,
    date: '6 hours ago',
  },
];

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <div className="space-y-6">
      {/* Welcome section */}
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">
          Welcome back, {user?.full_name}
        </h1>
        <p className="mt-1 text-sm text-gray-500">
          Here's what's happening with your pledges today.
        </p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((item) => (
          <div
            key={item.name}
            className="relative overflow-hidden rounded-lg bg-white px-4 pb-12 pt-5 shadow sm:px-6 sm:pt-6"
          >
            <dt>
              <div className="absolute rounded-md bg-blue-500 p-3">
                <item.icon className="h-6 w-6 text-white" aria-hidden="true" />
              </div>
              <p className="ml-16 truncate text-sm font-medium text-gray-500">
                {item.name}
              </p>
            </dt>
            <dd className="ml-16 flex items-baseline pb-6 sm:pb-7">
              <p className="text-2xl font-semibold text-gray-900">{item.value}</p>
              <p
                className={`ml-2 flex items-baseline text-sm font-semibold ${
                  item.changeType === 'increase' ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {item.changeType === 'increase' ? (
                  <ArrowUpIcon
                    className="h-5 w-5 flex-shrink-0 self-center text-green-500"
                    aria-hidden="true"
                  />
                ) : (
                  <ArrowDownIcon
                    className="h-5 w-5 flex-shrink-0 self-center text-red-500"
                    aria-hidden="true"
                  />
                )}
                <span className="sr-only">
                  {item.changeType === 'increase' ? 'Increased' : 'Decreased'} by
                </span>
                {item.change}
              </p>
            </dd>
          </div>
        ))}
      </div>

      {/* Recent activity */}
      <div className="bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:px-6">
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Recent Activity
          </h3>
        </div>
        <div className="border-t border-gray-200">
          <ul role="list" className="divide-y divide-gray-200">
            {recentActivity.map((activity) => (
              <li key={activity.id} className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      {activity.type === 'pledge' && (
                        <CurrencyDollarIcon className="h-5 w-5 text-green-500" />
                      )}
                      {activity.type === 'member' && (
                        <UserGroupIcon className="h-5 w-5 text-blue-500" />
                      )}
                      {activity.type === 'project' && (
                        <FolderIcon className="h-5 w-5 text-yellow-500" />
                      )}
                    </div>
                    <div className="ml-3">
                      <p className="text-sm font-medium text-gray-900">
                        {activity.description}
                      </p>
                      <p className="text-sm text-gray-500">{activity.date}</p>
                    </div>
                  </div>
                  {activity.amount && (
                    <div className="ml-2 flex-shrink-0 flex">
                      <p className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                        {activity.amount}
                      </p>
                    </div>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
} 