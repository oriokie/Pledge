import { User } from '@/types';

const BASE_URL = '/api/users';

export const users = {
  getAll: async (): Promise<User[]> => {
    const response = await fetch(BASE_URL);
    if (!response.ok) {
      throw new Error('Failed to fetch users');
    }
    return response.json();
  },

  getById: async (id: number): Promise<User> => {
    const response = await fetch(`${BASE_URL}/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch user');
    }
    return response.json();
  },

  create: async (data: Omit<User, 'id' | 'created_at' | 'updated_at'>): Promise<User> => {
    const response = await fetch(BASE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error('Failed to create user');
    }
    return response.json();
  },

  update: async (id: number, data: Partial<User>): Promise<User> => {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error('Failed to update user');
    }
    return response.json();
  },

  delete: async (id: number): Promise<void> => {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete user');
    }
  },
}; 