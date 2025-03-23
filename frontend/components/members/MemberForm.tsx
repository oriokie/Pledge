'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input, Select } from '@/components/ui/Form';
import { cn } from '@/lib/utils';

interface MemberFormData {
  name: string;
  email: string;
  phone: string;
  address: string;
  group?: string;
  status: 'active' | 'inactive';
}

interface MemberFormProps {
  member?: MemberFormData;
  onSubmit: (data: MemberFormData) => void;
  onCancel: () => void;
  className?: string;
}

export default function MemberForm({
  member,
  onSubmit,
  onCancel,
  className,
}: MemberFormProps) {
  const [formData, setFormData] = useState<MemberFormData>({
    name: '',
    email: '',
    phone: '',
    address: '',
    status: 'active',
    group: '',
  });

  const [errors, setErrors] = useState<Partial<MemberFormData>>({});

  useEffect(() => {
    if (member) {
      setFormData(member);
    }
  }, [member]);

  const validateForm = () => {
    const newErrors: Partial<MemberFormData> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error when user starts typing
    if (errors[name as keyof MemberFormData]) {
      setErrors((prev) => ({
        ...prev,
        [name]: undefined,
      }));
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className={cn('space-y-6', className)}
      noValidate
    >
      <div className="grid gap-6 md:grid-cols-2">
        <div>
          <Input
            label="Name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            error={errors.name}
            required
          />
        </div>
        <div>
          <Input
            label="Email"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            error={errors.email}
            required
          />
        </div>
        <div>
          <Input
            label="Phone"
            type="tel"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            error={errors.phone}
            required
          />
        </div>
        <div>
          <Select
            label="Status"
            name="status"
            value={formData.status}
            onChange={handleChange}
          >
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </Select>
        </div>
        <div className="md:col-span-2">
          <Input
            label="Address"
            name="address"
            value={formData.address}
            onChange={handleChange}
          />
        </div>
        <div className="md:col-span-2">
          <Select
            label="Group"
            name="group"
            value={formData.group}
            onChange={handleChange}
          >
            <option value="">Select a group</option>
            <option value="group1">Prayer Warriors</option>
            <option value="group2">Youth Ministry</option>
            <option value="group3">Choir</option>
          </Select>
        </div>
      </div>

      <div className="flex justify-end gap-4">
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit">
          {member ? 'Update Member' : 'Create Member'}
        </Button>
      </div>
    </form>
  );
} 