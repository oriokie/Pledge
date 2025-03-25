import { LoginCredentials, Token, User } from '@/types';

const BASE_URL = 'http://localhost:8000/api/v1';

export async function login(credentials: LoginCredentials): Promise<Token> {
  const formData = new URLSearchParams();
  formData.append('username', credentials.phone_number);
  formData.append('password', credentials.password);

  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Login failed');
  }

  return response.json();
}

export async function getCurrentUser(token: string): Promise<User> {
  const response = await fetch(`${BASE_URL}/auth/me`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get current user');
  }

  return response.json();
} 