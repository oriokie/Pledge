'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input, Select } from '@/components/ui/Form';
import { cn } from '@/lib/utils';

interface ProjectFormData {
  name: string;
  description: string;
  target: number;
  startDate: string;
  endDate: string;
  status: 'active' | 'completed' | 'cancelled';
}

interface ProjectFormProps {
  project?: ProjectFormData;
  onSubmit: (data: ProjectFormData) => void;
  onCancel: () => void;
  className?: string;
}

export default function ProjectForm({
  project,
  onSubmit,
  onCancel,
  className,
}: ProjectFormProps) {
  const [formData, setFormData] = useState<ProjectFormData>({
    name: '',
    description: '',
    target: 0,
    startDate: new Date().toISOString().split('T')[0],
    endDate: '',
    status: 'active',
  });

  const [errors, setErrors] = useState<Partial<ProjectFormData>>({});

  useEffect(() => {
    if (project) {
      setFormData(project);
    }
  }, [project]);

  const validateForm = () => {
    const newErrors: Partial<ProjectFormData> = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Project name is required';
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    }

    if (!formData.target || formData.target <= 0) {
      newErrors.target = 'Target amount must be greater than 0';
    }

    if (!formData.startDate) {
      newErrors.startDate = 'Start date is required';
    }

    if (!formData.endDate) {
      newErrors.endDate = 'End date is required';
    } else if (new Date(formData.endDate) <= new Date(formData.startDate)) {
      newErrors.endDate = 'End date must be after start date';
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
      [name]: name === 'target' ? parseFloat(value) || 0 : value,
    }));
    // Clear error when user starts typing
    if (errors[name as keyof ProjectFormData]) {
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
      <div className="grid gap-6">
        <div>
          <Input
            label="Project Name"
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
              label="Target Amount"
              type="number"
              name="target"
              value={formData.target}
              onChange={handleChange}
              error={errors.target}
              required
              min={0}
              step={0.01}
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
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </Select>
          </div>
          <div>
            <Input
              label="Start Date"
              type="date"
              name="startDate"
              value={formData.startDate}
              onChange={handleChange}
              error={errors.startDate}
              required
            />
          </div>
          <div>
            <Input
              label="End Date"
              type="date"
              name="endDate"
              value={formData.endDate}
              onChange={handleChange}
              error={errors.endDate}
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
          {project ? 'Update Project' : 'Create Project'}
        </Button>
      </div>
    </form>
  );
} 