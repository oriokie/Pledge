import { Pledge } from '@/types';

const BASE_URL = '/api/v1/pledges';

export const pledges = {
  getAll: async (): Promise<Pledge[]> => {
    const response = await fetch(BASE_URL, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });
    if (!response.ok) {
      throw new Error('Failed to fetch pledges');
    }
    return response.json();
  },

  getById: async (id: number): Promise<Pledge> => {
    const response = await fetch(`${BASE_URL}/${id}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });
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
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
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
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
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
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });
    if (!response.ok) {
      throw new Error('Failed to delete pledge');
    }
  },
}; 