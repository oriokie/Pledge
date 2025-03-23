'use client';

import * as React from 'react';
import { Card } from '@/components/ui/card';
import { BellIcon, KeyIcon, UserIcon, GlobeAltIcon } from '@heroicons/react/24/outline';

const settings = [
  {
    name: 'Profile Settings',
    description: 'Update your personal information and preferences',
    icon: UserIcon,
    href: '/settings/profile',
  },
  {
    name: 'Notifications',
    description: 'Configure your notification preferences',
    icon: BellIcon,
    href: '/settings/notifications',
  },
  {
    name: 'Security',
    description: 'Manage your password and security settings',
    icon: KeyIcon,
    href: '/settings/security',
  },
  {
    name: 'Language & Region',
    description: 'Set your preferred language and region',
    icon: GlobeAltIcon,
    href: '/settings/language',
  },
];

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900 dark:text-white">Settings</h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Manage your account settings and preferences
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
        {settings.map((setting) => (
          <Card key={setting.name} className="p-6">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <setting.icon className="h-6 w-6 text-gray-400" aria-hidden="true" />
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                  {setting.name}
                </h3>
                <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                  {setting.description}
                </p>
                <div className="mt-4">
                  <button
                    type="button"
                    className="text-sm font-medium text-primary hover:text-primary/90"
                  >
                    Configure
                  </button>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <Card className="p-6">
        <h2 className="text-lg font-medium text-gray-900 dark:text-white">System Information</h2>
        <dl className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <dt className="text-sm font-medium text-gray-500 dark:text-gray-400">Version</dt>
            <dd className="mt-1 text-sm text-gray-900 dark:text-white">1.0.0</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500 dark:text-gray-400">Last Updated</dt>
            <dd className="mt-1 text-sm text-gray-900 dark:text-white">March 15, 2024</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500 dark:text-gray-400">Database Size</dt>
            <dd className="mt-1 text-sm text-gray-900 dark:text-white">2.5 GB</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500 dark:text-gray-400">Active Users</dt>
            <dd className="mt-1 text-sm text-gray-900 dark:text-white">150</dd>
          </div>
        </dl>
      </Card>

      <Card className="p-6">
        <h2 className="text-lg font-medium text-gray-900 dark:text-white">Backup & Restore</h2>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Manage your system backups and restore points
        </p>
        <div className="mt-4 flex gap-4">
          <button
            type="button"
            className="inline-flex items-center rounded-md bg-primary px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
          >
            Create Backup
          </button>
          <button
            type="button"
            className="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 dark:bg-gray-800 dark:text-white dark:ring-gray-700 dark:hover:bg-gray-700"
          >
            Restore Backup
          </button>
        </div>
      </Card>
    </div>
  );
} 