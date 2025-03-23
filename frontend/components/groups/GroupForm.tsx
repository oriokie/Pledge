'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input, Select } from '@/components/ui/Form';
import { cn } from '@/lib/utils';

interface GroupFormData {
  name: string;
  description: string;
  leader: string;
  meetingDay: string;
  meetingTime: string;
  status: 'active' | 'inactive';
}

interface GroupFormProps {
  group?: GroupFormData;
  onSubmit: (data: GroupFormData) => void;
  onCancel: () => void;
  className?: string;
}

export default function GroupForm({
  group,
  onSubmit,
  onCancel,
  className,
}: GroupFormProps) {
  const [formData, setFormData] = useState<GroupFormData>({
    name: '',
    description: '',
    leader: '',
    meetingDay: '',
    meetingTime: '',
    status: 'active',
  });

  const [errors, setErrors] = useState<Partial<GroupFormData>>({});

  useEffect(() => {
    if (group) {
      setFormData(group);
    }
  }, [group]);

  const validateForm = () => {
    const newErrors: Partial<GroupFormData> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Group name is required';
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    }

    if (!formData.leader.trim()) {
      newErrors.leader = 'Leader is required';
    }

    if (!formData.meetingDay) {
      newErrors.meetingDay = 'Meeting day is required';
    }

    if (!formData.meetingTime) {
      newErrors.meetingTime = 'Meeting time is required';
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
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error when user starts typing
    if (errors[name as keyof GroupFormData]) {
      setErrors((prev) => ({
        ...prev,
        [name]: undefined,
      }));
    }
  };

  const daysOfWeek = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday',
  ];

  return (
    <form
      onSubmit={handleSubmit}
      className={cn('space-y-6', className)}
      noValidate
    >
      <div className="grid gap-6">
        <div>
          <Input
            label="Group Name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            error={errors.name}
            required
          />
        </div>
        <div>
          <Input
            label="Description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            error={errors.description}
            required
            multiline
            rows={4}
          />
        </div>
        <div className="grid gap-6 md:grid-cols-2">
          <div>
            <Input
              label="Leader"
              name="leader"
              value={formData.leader}
              onChange={handleChange}
              error={errors.leader}
              required
            />
          </div>
          <div>
            <Select
              label="Status"
              name="status"
              value={formData.status}
              onChange={handleChange}
              required
            >
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </Select>
          </div>
          <div>
            <Select
              label="Meeting Day"
              name="meetingDay"
              value={formData.meetingDay}
              onChange={handleChange}
              error={errors.meetingDay}
              required
            >
              <option value="">Select a day</option>
              {daysOfWeek.map((day) => (
                <option key={day} value={day}>
                  {day}
                </option>
              ))}
            </Select>
          </div>
          <div>
            <Input
              label="Meeting Time"
              type="time"
              name="meetingTime"
              value={formData.meetingTime}
              onChange={handleChange}
              error={errors.meetingTime}
              required
            />
          </div>
        </div>
      </div>

      <div className="flex justify-end gap-4">
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit">
          {group ? 'Update Group' : 'Create Group'}
        </Button>
      </div>
    </form>
  );
} 