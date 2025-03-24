import { Contribution } from '@/types';

const BASE_URL = '/api/contributions';

export const contributions = {
  getAll: async (): Promise<Contribution[]> => {
    const response = await fetch(BASE_URL);
    if (!response.ok) {
      throw new Error('Failed to fetch contributions');
    }
    return response.json();
  },

  getById: async (id: number): Promise<Contribution> => {
    const response = await fetch(`${BASE_URL}/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch contribution');
    }
    return response.json();
  },

  create: async (data: Omit<Contribution, 'id' | 'created_at' | 'updated_at'>): Promise<Contribution> => {
    const response = await fetch(BASE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error('Failed to create contribution');
    }
    return response.json();
  },

  update: async (id: number, data: Partial<Contribution>): Promise<Contribution> => {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error('Failed to update contribution');
    }
    return response.json();
  },

  delete: async (id: number): Promise<void> => {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete contribution');
    }
  },
}; 