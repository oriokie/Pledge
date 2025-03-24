import { User } from '@/types';

const BASE_URL = '/api/v1/auth';

export const auth = {
  login: async (username: string, password: string): Promise<{ access_token: string; token_type: string }> => {
    const response = await fetch(`${BASE_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username,
        password,
      }).toString(),
    });
    if (!response.ok) {
      throw new Error('Failed to authenticate');
    }
    return response.json();
  },

  me: async (): Promise<User> => {
    const response = await fetch(`${BASE_URL}/me`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });
    if (!response.ok) {
      throw new Error('Failed to get user profile');
    }
    return response.json();
  },

  testToken: async (): Promise<User> => {
    const response = await fetch(`${BASE_URL}/test-token`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });
    if (!response.ok) {
      throw new Error('Failed to validate token');
    }
    return response.json();
  },
}; 