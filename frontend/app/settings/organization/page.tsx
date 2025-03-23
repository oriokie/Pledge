'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Form';
import { ColorPicker } from '@/components/ui/ColorPicker';
import { FileUpload } from '@/components/ui/FileUpload';

interface OrganizationSettings {
  name: string;
  email: string;
  phone: string;
  address: string;
  logo: string;
  primaryColor: string;
  secondaryColor: string;
  timezone: string;
  currency: string;
}

export default function OrganizationSettingsPage() {
  const [settings, setSettings] = useState<OrganizationSettings>({
    name: 'Example Church',
    email: 'contact@example.com',
    phone: '+1 (555) 123-4567',
    address: '123 Main St, City, State 12345',
    logo: '/logo.png',
    primaryColor: '#4F46E5',
    secondaryColor: '#10B981',
    timezone: 'America/New_York',
    currency: 'USD',
  });

  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      // TODO: Implement API call to save settings
      await new Promise((resolve) => setTimeout(resolve, 1000)); // Simulate API call
      console.log('Saving settings:', settings);
    } catch (error) {
      console.error('Error saving settings:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (
    name: keyof OrganizationSettings,
    value: string
  ) => {
    setSettings((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleLogoUpload = (file: File) => {
    // TODO: Implement logo upload
    console.log('Uploading logo:', file);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          Organization Settings
        </h1>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Manage your organization's profile and preferences
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        <div className="grid gap-6 md:grid-cols-2">
          <div className="col-span-2">
            <FileUpload
              label="Organization Logo"
              accept="image/*"
              onUpload={handleLogoUpload}
              preview={settings.logo}
              maxSize={5 * 1024 * 1024} // 5MB
            />
          </div>
          <div>
            <Input
              label="Organization Name"
              value={settings.name}
              onChange={(e) => handleChange('name', e.target.value)}
              required
            />
          </div>
          <div>
            <Input
              label="Email Address"
              type="email"
              value={settings.email}
              onChange={(e) => handleChange('email', e.target.value)}
              required
            />
          </div>
          <div>
            <Input
              label="Phone Number"
              type="tel"
              value={settings.phone}
              onChange={(e) => handleChange('phone', e.target.value)}
              required
            />
          </div>
          <div>
            <Input
              label="Address"
              value={settings.address}
              onChange={(e) => handleChange('address', e.target.value)}
              required
            />
          </div>
          <div>
            <ColorPicker
              label="Primary Color"
              value={settings.primaryColor}
              onChange={(value) => handleChange('primaryColor', value)}
            />
          </div>
          <div>
            <ColorPicker
              label="Secondary Color"
              value={settings.secondaryColor}
              onChange={(value) => handleChange('secondaryColor', value)}
            />
          </div>
          <div>
            <Input
              label="Timezone"
              value={settings.timezone}
              onChange={(e) => handleChange('timezone', e.target.value)}
              required
            />
          </div>
          <div>
            <Input
              label="Currency"
              value={settings.currency}
              onChange={(e) => handleChange('currency', e.target.value)}
              required
            />
          </div>
        </div>

        <div className="flex justify-end">
          <Button type="submit" isLoading={isLoading}>
            Save Changes
          </Button>
        </div>
      </form>
    </div>
  );
} 