import { Pledge } from '@/types';

const BASE_URL = '/api/pledges';

export const pledges = {
  getAll: async (): Promise<Pledge[]> => {
    const response = await fetch(BASE_URL);
    if (!response.ok) {
      throw new Error('Failed to fetch pledges');
    }
    return response.json();
  },

  getById: async (id: number): Promise<Pledge> => {
    const response = await fetch(`${BASE_URL}/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch pledge');
    }
    return response.json();
  },

  create: async (data: Omit<Pledge, 'id' | 'created_at' | 'updated_at'>): Promise<Pledge> => {
    const response = await fetch(BASE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error('Failed to create pledge');
    }
    return response.json();
  },

  update: async (id: number, data: Partial<Pledge>): Promise<Pledge> => {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error('Failed to update pledge');
    }
    return response.json();
  },

  delete: async (id: number): Promise<void> => {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete pledge');
    }
  },
}; 