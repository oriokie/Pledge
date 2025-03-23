'use client';

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/Button';
import { Input, Select } from '@/components/ui/Form';
import { cn } from '@/lib/utils';

interface ContributionFormData {
  memberId: string;
  amount: number;
  type: 'tithe' | 'offering' | 'project' | 'other';
  project?: string;
  paymentMethod: 'cash' | 'card' | 'bank_transfer' | 'mobile_money';
  date: string;
  notes?: string;
}

interface ContributionFormProps {
  contribution?: ContributionFormData;
  onSubmit: (data: ContributionFormData) => void;
  onCancel: () => void;
  className?: string;
}

export default function ContributionForm({
  contribution,
  onSubmit,
  onCancel,
  className,
}: ContributionFormProps) {
  const [formData, setFormData] = useState<ContributionFormData>({
    memberId: '',
    amount: 0,
    type: 'tithe',
    paymentMethod: 'cash',
    date: new Date().toISOString().split('T')[0],
  });

  const [errors, setErrors] = useState<Partial<ContributionFormData>>({});

  useEffect(() => {
    if (contribution) {
      setFormData(contribution);
    }
  }, [contribution]);

  const validateForm = () => {
    const newErrors: Partial<ContributionFormData> = {};

    if (!formData.memberId) {
      newErrors.memberId = 'Member is required';
    }

    if (!formData.amount || formData.amount <= 0) {
      newErrors.amount = 'Amount must be greater than 0';
    }

    if (!formData.date) {
      newErrors.date = 'Date is required';
    }

    if (formData.type === 'project' && !formData.project) {
      newErrors.project = 'Project is required for project contributions';
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
      [name]: name === 'amount' ? parseFloat(value) || 0 : value,
    }));
    // Clear error when user starts typing
    if (errors[name as keyof ContributionFormData]) {
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
          <Select
            label="Member"
            name="memberId"
            value={formData.memberId}
            onChange={handleChange}
            error={errors.memberId}
            required
          >
            <option value="">Select a member</option>
            {/* TODO: Replace with actual member data */}
            <option value="1">John Doe</option>
            <option value="2">Jane Smith</option>
          </Select>
        </div>
        <div>
          <Input
            label="Amount"
            type="number"
            name="amount"
            value={formData.amount}
            onChange={handleChange}
            error={errors.amount}
            required
            min={0}
            step={0.01}
          />
        </div>
        <div>
          <Select
            label="Type"
            name="type"
            value={formData.type}
            onChange={handleChange}
            required
          >
            <option value="tithe">Tithe</option>
            <option value="offering">Offering</option>
            <option value="project">Project</option>
            <option value="other">Other</option>
          </Select>
        </div>
        {formData.type === 'project' && (
          <div>
            <Select
              label="Project"
              name="project"
              value={formData.project}
              onChange={handleChange}
              error={errors.project}
              required
            >
              <option value="">Select a project</option>
              {/* TODO: Replace with actual project data */}
              <option value="1">Church Building Fund</option>
              <option value="2">Mission Trip</option>
              <option value="3">Youth Center</option>
            </Select>
          </div>
        )}
        <div>
          <Select
            label="Payment Method"
            name="paymentMethod"
            value={formData.paymentMethod}
            onChange={handleChange}
            required
          >
            <option value="cash">Cash</option>
            <option value="card">Card</option>
            <option value="bank_transfer">Bank Transfer</option>
            <option value="mobile_money">Mobile Money</option>
          </Select>
        </div>
        <div>
          <Input
            label="Date"
            type="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            error={errors.date}
            required
          />
        </div>
        <div className="md:col-span-2">
          <Input
            label="Notes"
            name="notes"
            value={formData.notes}
            onChange={handleChange}
            multiline
            rows={3}
          />
        </div>
      </div>

      <div className="flex justify-end gap-4">
        <Button type="button" variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit">
          {contribution ? 'Update Contribution' : 'Create Contribution'}
        </Button>
      </div>
    </form>
  );
} 