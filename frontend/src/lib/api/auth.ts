import { LoginCredentials, Token, User } from '@/types';

const BASE_URL = '/api/auth';

export const auth = {
  login: async (credentials: LoginCredentials): Promise<Token> => {
    const response = await fetch(`${BASE_URL}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    if (!response.ok) {
      throw new Error('Failed to login');
    }
    return response.json();
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await fetch(`${BASE_URL}`);
    if (!response.ok) {
      throw new Error('Failed to fetch current user');
    }
    return response.json();
  },
}; 