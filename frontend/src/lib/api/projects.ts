import { Project } from '@/types';

const BASE_URL = '/api/projects';

export const projects = {
  getAll: async (): Promise<Project[]> => {
    const response = await fetch(BASE_URL);
    if (!response.ok) {
      throw new Error('Failed to fetch projects');
    }
    return response.json();
  },

  getById: async (id: number): Promise<Project> => {
    const response = await fetch(`${BASE_URL}/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch project');
    }
    return response.json();
  },

  create: async (data: Omit<Project, 'id' | 'created_at' | 'updated_at'>): Promise<Project> => {
    const response = await fetch(BASE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error('Failed to create project');
    }
    return response.json();
  },

  update: async (id: number, data: Partial<Project>): Promise<Project> => {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error('Failed to update project');
    }
    return response.json();
  },

  delete: async (id: number): Promise<void> => {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete project');
    }
  },
}; 