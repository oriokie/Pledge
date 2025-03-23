'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Input, Select } from '@/components/ui/Form';

interface NotificationSettings {
  emailFrequency: 'instant' | 'daily' | 'weekly' | 'never';
  pushNotifications: boolean;
  desktopNotifications: boolean;
  notifyOn: {
    newContributions: boolean;
    contributionReminders: boolean;
    projectUpdates: boolean;
    groupAnnouncements: boolean;
    eventReminders: boolean;
    systemUpdates: boolean;
  };
  quietHours: {
    enabled: boolean;
    start: string;
    end: string;
  };
}

export default function NotificationSettingsPage() {
  const [settings, setSettings] = useState<NotificationSettings>({
    emailFrequency: 'daily',
    pushNotifications: true,
    desktopNotifications: true,
    notifyOn: {
      newContributions: true,
      contributionReminders: true,
      projectUpdates: true,
      groupAnnouncements: true,
      eventReminders: true,
      systemUpdates: true,
    },
    quietHours: {
      enabled: false,
      start: '22:00',
      end: '07:00',
    },
  });

  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // TODO: Implement API call to save settings
      await new Promise((resolve) => setTimeout(resolve, 1000)); // Simulate API call
      console.log('Saving notification settings:', settings);
    } catch (error) {
      console.error('Error saving settings:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (
    name: string,
    value: any,
    category?: 'notifyOn' | 'quietHours'
  ) => {
    setSettings((prev) => {
      if (category === 'notifyOn') {
        return {
          ...prev,
          notifyOn: {
            ...prev.notifyOn,
            [name]: value,
          },
        };
      }
      if (category === 'quietHours') {
        return {
          ...prev,
          quietHours: {
            ...prev.quietHours,
            [name]: value,
          },
        };
      }
      return {
        ...prev,
        [name]: value,
      };
    });
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Notification Settings
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Manage how and when you receive notifications
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        <div className="space-y-6">
          <div>
            <h2 className="text-lg font-medium text-gray-900 dark:text-white">
              Delivery Preferences
            </h2>
            <div className="mt-4 space-y-4">
              <Select
                label="Email Frequency"
                value={settings.emailFrequency}
                onChange={(e: React.ChangeEvent<HTMLSelectElement>) => handleChange('emailFrequency', e.target.value)}
              >
                <option value="instant">Instant</option>
                <option value="daily">Daily Digest</option>
                <option value="weekly">Weekly Digest</option>
                <option value="never">Never</option>
              </Select>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="push-notifications"
                  checked={settings.pushNotifications}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    handleChange('pushNotifications', e.target.checked)
                  }
                  className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                />
                <label
                  htmlFor="push-notifications"
                  className="ml-2 text-sm text-gray-900 dark:text-white"
                >
                  Enable Push Notifications
                </label>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="desktop-notifications"
                  checked={settings.desktopNotifications}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    handleChange('desktopNotifications', e.target.checked)
                  }
                  className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                />
                <label
                  htmlFor="desktop-notifications"
                  className="ml-2 text-sm text-gray-900 dark:text-white"
                >
                  Enable Desktop Notifications
                </label>
              </div>
            </div>
          </div>

          <div>
            <h2 className="text-lg font-medium text-gray-900 dark:text-white">
              Notification Types
            </h2>
            <div className="mt-4 space-y-4">
              {Object.entries(settings.notifyOn).map(([key, value]) => (
                <div key={key} className="flex items-center">
                  <input
                    type="checkbox"
                    id={key}
                    checked={value}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                      handleChange(key, e.target.checked, 'notifyOn')
                    }
                    className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                  />
                  <label
                    htmlFor={key}
                    className="ml-2 text-sm text-gray-900 dark:text-white"
                  >
                    {key
                      .replace(/([A-Z])/g, ' $1')
                      .replace(/^./, (str) => str.toUpperCase())}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-lg font-medium text-gray-900 dark:text-white">
              Quiet Hours
            </h2>
            <div className="mt-4 space-y-4">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="quiet-hours-enabled"
                  checked={settings.quietHours.enabled}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    handleChange('enabled', e.target.checked, 'quietHours')
                  }
                  className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
                />
                <label
                  htmlFor="quiet-hours-enabled"
                  className="ml-2 text-sm text-gray-900 dark:text-white"
                >
                  Enable Quiet Hours
                </label>
              </div>

              {settings.quietHours.enabled && (
                <div className="grid gap-4 md:grid-cols-2">
                  <Input
                    type="time"
                    label="Start Time"
                    value={settings.quietHours.start}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                      handleChange('start', e.target.value, 'quietHours')
                    }
                  />
                  <Input
                    type="time"
                    label="End Time"
                    value={settings.quietHours.end}
                    onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                      handleChange('end', e.target.value, 'quietHours')
                    }
                  />
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="flex justify-end">
          <Button type="submit" isLoading={isLoading}>
            Save Settings
          </Button>
        </div>
      </form>
    </div>
  );
} 