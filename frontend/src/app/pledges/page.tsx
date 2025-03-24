'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { pledges } from '@/lib/api';
import { Pledge } from '@/types';
import { useAuth } from '@/contexts/AuthContext';
import toast from 'react-hot-toast';

export default function PledgesPage() {
  const queryClient = useQueryClient();
  const { user: currentUser } = useAuth();
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingPledge, setEditingPledge] = useState<Pledge | null>(null);

  const { data: pledgesData, isLoading } = useQuery({
    queryKey: ['pledges'],
    queryFn: pledges.getAll,
  });

  const createMutation = useMutation({
    mutationFn: pledges.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pledges'] });
      setIsCreateModalOpen(false);
      toast.success('Pledge created successfully');
    },
    onError: () => {
      toast.error('Failed to create pledge');
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Pledge> }) =>
      pledges.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pledges'] });
      setEditingPledge(null);
      toast.success('Pledge updated successfully');
    },
    onError: () => {
      toast.error('Failed to update pledge');
    },
  });

  const deleteMutation = useMutation({
    mutationFn: pledges.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pledges'] });
      toast.success('Pledge deleted successfully');
    },
    onError: () => {
      toast.error('Failed to delete pledge');
    },
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold text-gray-900">Pledges</h1>
        {currentUser?.role !== 'MEMBER' && (
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Add Pledge
          </button>
        )}
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul role="list" className="divide-y divide-gray-200">
          {pledgesData?.map((pledge) => (
            <li key={pledge.id}>
              <div className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm font-medium text-gray-900">
                      {pledge.description}
                    </div>
                    <div className="text-sm text-gray-500">
                      Amount: ${pledge.amount.toFixed(2)}
                    </div>
                    <div className="text-sm text-gray-500">
                      Due Date: {new Date(pledge.due_date).toLocaleDateString()}
                    </div>
                    <div className="text-sm text-gray-500">
                      Status: {pledge.status}
                    </div>
                  </div>
                  {currentUser?.role !== 'MEMBER' && (
                    <div className="flex space-x-2">
                      <button
                        onClick={() => setEditingPledge(pledge)}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => {
                          if (window.confirm('Are you sure you want to delete this pledge?')) {
                            deleteMutation.mutate(pledge.id);
                          }
                        }}
                        className="text-red-600 hover:text-red-900"
                      >
                        Delete
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>

      {/* Create Pledge Modal */}
      {isCreateModalOpen && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-lg font-medium mb-4">Create Pledge</h2>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                const formData = new FormData(e.currentTarget);
                createMutation.mutate({
                  amount: parseFloat(formData.get('amount') as string),
                  description: formData.get('description') as string,
                  due_date: new Date(formData.get('due_date') as string),
                  status: 'PENDING',
                });
              }}
              className="space-y-4"
            >
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Amount
                </label>
                <input
                  type="number"
                  name="amount"
                  step="0.01"
                  required
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Description
                </label>
                <textarea
                  name="description"
                  required
                  rows={3}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Due Date
                </label>
                <input
                  type="date"
                  name="due_date"
                  required
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setIsCreateModalOpen(false)}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Pledge Modal */}
      {editingPledge && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-lg font-medium mb-4">Edit Pledge</h2>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                const formData = new FormData(e.currentTarget);
                updateMutation.mutate({
                  id: editingPledge.id,
                  data: {
                    amount: parseFloat(formData.get('amount') as string),
                    description: formData.get('description') as string,
                    due_date: new Date(formData.get('due_date') as string),
                    status: formData.get('status') as Pledge['status'],
                  },
                });
              }}
              className="space-y-4"
            >
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Amount
                </label>
                <input
                  type="number"
                  name="amount"
                  step="0.01"
                  defaultValue={editingPledge.amount}
                  required
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Description
                </label>
                <textarea
                  name="description"
                  defaultValue={editingPledge.description}
                  required
                  rows={3}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Due Date
                </label>
                <input
                  type="date"
                  name="due_date"
                  defaultValue={new Date(editingPledge.due_date).toISOString().split('T')[0]}
                  required
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Status
                </label>
                <select
                  name="status"
                  defaultValue={editingPledge.status}
                  required
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                >
                  <option value="PENDING">Pending</option>
                  <option value="PAID">Paid</option>
                  <option value="CANCELLED">Cancelled</option>
                </select>
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setEditingPledge(null)}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700"
                >
                  Save
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
} 