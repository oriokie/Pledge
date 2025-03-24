import { File } from '@/types';

const BASE_URL = '/api/files';

export const files = {
  getAll: async (): Promise<File[]> => {
    const response = await fetch(BASE_URL);
    if (!response.ok) {
      throw new Error('Failed to fetch files');
    }
    return response.json();
  },

  getById: async (id: number): Promise<File> => {
    const response = await fetch(`${BASE_URL}/${id}`);
    if (!response.ok) {
      throw new Error('Failed to fetch file');
    }
    return response.json();
  },

  upload: async (file: File): Promise<File> => {
    const formData = new FormData();
    formData.append('file', file as any);

    const response = await fetch(BASE_URL, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
      throw new Error('Failed to upload file');
    }
    return response.json();
  },

  delete: async (id: number): Promise<void> => {
    const response = await fetch(`${BASE_URL}/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete file');
    }
  },
}; 