import { Report } from '@/types';

const BASE_URL = '/api/reports';

export const reports = {
  getAll: async (): Promise<Report[]> => {
    const response = await fetch(BASE_URL);
    if (!response.ok) {
      throw new Error('Failed to fetch reports');
    }
    return response.json();
  },

  getById: async (id: number): Promise<Report> => {
    const response = await fetch(`${BASE_URL}/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch report');
    }
    return response.json();
  },

  create: async (data: Omit<Report, 'id' | 'created_at' | 'updated_at'>): Promise<Report> => {
    const response = await fetch(BASE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error('Failed to create report');
    }
    return response.json();
  },

  update: async (id: number, data: Partial<Report>): Promise<Report> => {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error('Failed to update report');
    }
    return response.json();
  },

  delete: async (id: number): Promise<void> => {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete report');
    }
  },

  generate: async (reportType: Report['report_type'], parameters: Record<string, any>): Promise<Report> => {
    const response = await fetch(`${BASE_URL}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ report_type: reportType, parameters }),
    });
    if (!response.ok) {
      throw new Error('Failed to generate report');
    }
    return response.json();
  },
}; 