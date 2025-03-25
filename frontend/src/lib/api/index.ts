import axios from 'axios';
import { Member, Project, Contribution } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to add the auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Auth API
export const login = async (phone_number: string, password: string) => {
  const formData = new URLSearchParams();
  formData.append('username', phone_number);
  formData.append('password', password);

  const response = await apiClient.post('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data;
};

export const logout = async () => {
  const response = await apiClient.post('/auth/logout');
  return response.data;
};

// Members API
export const getMembers = async (): Promise<Member[]> => {
  const response = await apiClient.get('/members');
  return response.data;
};

export const createMember = async (data: Omit<Member, 'id' | 'created_at' | 'updated_at'>): Promise<Member> => {
  const response = await apiClient.post('/members', data);
  return response.data;
};

export const updateMember = async (id: number, data: Partial<Member>): Promise<Member> => {
  const response = await apiClient.put(`/members/${id}`, data);
  return response.data;
};

export const deleteMember = async (id: number): Promise<void> => {
  await apiClient.delete(`/members/${id}`);
};

// Projects API
export const getProjects = async (): Promise<Project[]> => {
  const response = await apiClient.get('/projects');
  return response.data;
};

export const createProject = async (data: Omit<Project, 'id' | 'created_at' | 'updated_at'>): Promise<Project> => {
  const response = await apiClient.post('/projects', data);
  return response.data;
};

export const updateProject = async (id: number, data: Partial<Project>): Promise<Project> => {
  const response = await apiClient.put(`/projects/${id}`, data);
  return response.data;
};

export const deleteProject = async (id: number): Promise<void> => {
  await apiClient.delete(`/projects/${id}`);
};

// Contributions API
export const getContributions = async (): Promise<Contribution[]> => {
  const response = await apiClient.get('/contributions');
  return response.data;
};

export const createContribution = async (data: Omit<Contribution, 'id' | 'created_at' | 'updated_at'>): Promise<Contribution> => {
  const response = await apiClient.post('/contributions', data);
  return response.data;
};

export const updateContribution = async (id: number, data: Partial<Contribution>): Promise<Contribution> => {
  const response = await apiClient.put(`/contributions/${id}`, data);
  return response.data;
};

export const deleteContribution = async (id: number): Promise<void> => {
  await apiClient.delete(`/contributions/${id}`);
}; 