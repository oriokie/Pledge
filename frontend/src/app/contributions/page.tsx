'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { contributions } from '@/lib/api';
import { Contribution } from '@/types';
import { useAuth } from '@/contexts/AuthContext';
import toast from 'react-hot-toast';

export default function ContributionsPage() {
  const queryClient = useQueryClient();
  const { user: currentUser } = useAuth();
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingContribution, setEditingContribution] = useState<Contribution | null>(null);

  const { data: contributionsData, isLoading } = useQuery({
    queryKey: ['contributions'],
    queryFn: contributions.getAll,
  });

  const createMutation = useMutation({
    mutationFn: contributions.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['contributions'] });
      setIsCreateModalOpen(false);
      toast.success('Contribution created successfully');
    },
    onError: () => {
      toast.error('Failed to create contribution');
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<Contribution> }) =>
      contributions.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['contributions'] });
      setEditingContribution(null);
      toast.success('Contribution updated successfully');
    },
    onError: () => {
      toast.error('Failed to update contribution');
    },
  });

  const deleteMutation = useMutation({
    mutationFn: contributions.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['contributions'] });
      toast.success('Contribution deleted successfully');
    },
    onError: () => {
      toast.error('Failed to delete contribution');
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
        <h1 className="text-2xl font-semibold text-gray-900">Contributions</h1>
        {currentUser?.role !== 'MEMBER' && (
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Add Contribution
          </button>
        )}
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul role="list" className="divide-y divide-gray-200">
          {contributionsData?.map((contribution) => (
            <li key={contribution.id}>
              <div className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="text-sm font-medium text-gray-900">
                      {contribution.description}
                    </div>
                    <div className="text-sm text-gray-500">
                      Amount: ${contribution.amount.toFixed(2)}
                    </div>
                    <div className="text-sm text-gray-500">
                      Date: {new Date(contribution.created_at).toLocaleDateString()}
                    </div>
                  </div>
                  {currentUser?.role !== 'MEMBER' && (
                    <div className="flex space-x-2">
                      <button
                        onClick={() => setEditingContribution(contribution)}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => {
                          if (window.confirm('Are you sure you want to delete this contribution?')) {
                            deleteMutation.mutate(contribution.id);
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

      {/* Create Contribution Modal */}
      {isCreateModalOpen && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-lg font-medium mb-4">Create Contribution</h2>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                const formData = new FormData(e.currentTarget);
                createMutation.mutate({
                  amount: parseFloat(formData.get('amount') as string),
                  description: formData.get('description') as string,
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

      {/* Edit Contribution Modal */}
      {editingContribution && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-lg font-medium mb-4">Edit Contribution</h2>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                const formData = new FormData(e.currentTarget);
                updateMutation.mutate({
                  id: editingContribution.id,
                  data: {
                    amount: parseFloat(formData.get('amount') as string),
                    description: formData.get('description') as string,
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
                  defaultValue={editingContribution.amount}
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
                  defaultValue={editingContribution.description}
                  required
                  rows={3}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setEditingContribution(null)}
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