import axios from 'axios';
import { LoginCredentials, Token, User, Contribution, Pledge, Member, Group } from '@/types';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Enable sending cookies with requests
});

// Add token to requests if it exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const auth = {
  login: async (credentials: LoginCredentials): Promise<Token> => {
    const response = await api.post('/auth/login', credentials);
    return response.data;
  },
  
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

export const users = {
  getAll: async (): Promise<User[]> => {
    const response = await api.get('/users');
    return response.data;
  },
  
  getById: async (id: number): Promise<User> => {
    const response = await api.get(`/users/${id}`);
    return response.data;
  },
  
  create: async (user: Omit<User, 'id' | 'created_at' | 'updated_at'>): Promise<User> => {
    const response = await api.post('/users', user);
    return response.data;
  },
  
  update: async (id: number, user: Partial<User> | { password: string }): Promise<User> => {
    const response = await api.put(`/users/${id}`, user);
    return response.data;
  },
  
  delete: async (id: number): Promise<void> => {
    await api.delete(`/users/${id}`);
  },
};

export const members = {
  getAll: async (): Promise<Member[]> => {
    const response = await api.get('/members');
    return response.data;
  },
  
  getById: async (id: number): Promise<Member> => {
    const response = await api.get(`/members/${id}`);
    return response.data;
  },
  
  create: async (member: Omit<Member, 'id' | 'created_at' | 'updated_at'>): Promise<Member> => {
    const response = await api.post('/members', member);
    return response.data;
  },
  
  update: async (id: number, member: Partial<Member>): Promise<Member> => {
    const response = await api.put(`/members/${id}`, member);
    return response.data;
  },
  
  delete: async (id: number): Promise<void> => {
    await api.delete(`/members/${id}`);
  },
};

export const contributions = {
  getAll: async (): Promise<Contribution[]> => {
    const response = await api.get('/contributions');
    return response.data;
  },
  
  getById: async (id: number): Promise<Contribution> => {
    const response = await api.get(`/contributions/${id}`);
    return response.data;
  },
  
  create: async (contribution: Omit<Contribution, 'id' | 'created_at' | 'updated_at'>): Promise<Contribution> => {
    const response = await api.post('/contributions', contribution);
    return response.data;
  },
  
  update: async (id: number, contribution: Partial<Contribution>): Promise<Contribution> => {
    const response = await api.put(`/contributions/${id}`, contribution);
    return response.data;
  },
  
  delete: async (id: number): Promise<void> => {
    await api.delete(`/contributions/${id}`);
  },
};

export const pledges = {
  getAll: async (): Promise<Pledge[]> => {
    const response = await api.get('/pledges');
    return response.data;
  },
  
  getById: async (id: number): Promise<Pledge> => {
    const response = await api.get(`/pledges/${id}`);
    return response.data;
  },
  
  create: async (pledge: Omit<Pledge, 'id' | 'created_at' | 'updated_at'>): Promise<Pledge> => {
    const response = await api.post('/pledges', pledge);
    return response.data;
  },
  
  update: async (id: number, pledge: Partial<Pledge>): Promise<Pledge> => {
    const response = await api.put(`/pledges/${id}`, pledge);
    return response.data;
  },
  
  delete: async (id: number): Promise<void> => {
    await api.delete(`/pledges/${id}`);
  },
};

export const groups = {
  getAll: async (): Promise<Group[]> => {
    const response = await api.get('/groups');
    return response.data;
  },
  
  getById: async (id: number): Promise<Group> => {
    const response = await api.get(`/groups/${id}`);
    return response.data;
  },
  
  create: async (group: Omit<Group, 'id' | 'created_at' | 'updated_at'>): Promise<Group> => {
    const response = await api.post('/groups', group);
    return response.data;
  },
  
  update: async (id: number, group: Partial<Group>): Promise<Group> => {
    const response = await api.put(`/groups/${id}`, group);
    return response.data;
  },
  
  delete: async (id: number): Promise<void> => {
    await api.delete(`/groups/${id}`);
  },
}; 