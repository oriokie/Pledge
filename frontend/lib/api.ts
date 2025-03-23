import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login', { email, password });
    localStorage.setItem('token', response.data.token);
    return response.data;
  },
  logout: () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  },
  register: async (data: {
    email: string;
    password: string;
    name: string;
    phone: string;
  }) => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },
  getProfile: async () => {
    const response = await api.get('/auth/profile');
    return response.data;
  },
  updateProfile: async (data: {
    name?: string;
    email?: string;
    phone?: string;
    current_password?: string;
    new_password?: string;
  }) => {
    const response = await api.put('/auth/profile', data);
    return response.data;
  },
};

// Members API
export const membersAPI = {
  getAll: async (params?: {
    search?: string;
    status?: string;
    page?: number;
    limit?: number;
  }) => {
    const response = await api.get('/members', { params });
    return response.data;
  },
  getById: async (id: string) => {
    const response = await api.get(`/members/${id}`);
    return response.data;
  },
  create: async (data: {
    name: string;
    email: string;
    phone: string;
    address: string;
    status: string;
  }) => {
    const response = await api.post('/members', data);
    return response.data;
  },
  update: async (id: string, data: {
    name?: string;
    email?: string;
    phone?: string;
    address?: string;
    status?: string;
  }) => {
    const response = await api.put(`/members/${id}`, data);
    return response.data;
  },
  delete: async (id: string) => {
    const response = await api.delete(`/members/${id}`);
    return response.data;
  },
};

// Contributions API
export const contributionsAPI = {
  getAll: async (params?: {
    search?: string;
    status?: string;
    group_id?: string;
    page?: number;
    limit?: number;
  }) => {
    const response = await api.get('/contributions', { params });
    return response.data;
  },
  getById: async (id: string) => {
    const response = await api.get(`/contributions/${id}`);
    return response.data;
  },
  create: async (data: {
    member_id: string;
    amount: number;
    payment_method: string;
    status: string;
    group_id?: string;
  }) => {
    const response = await api.post('/contributions', data);
    return response.data;
  },
  update: async (id: string, data: {
    amount?: number;
    payment_method?: string;
    status?: string;
    group_id?: string;
  }) => {
    const response = await api.put(`/contributions/${id}`, data);
    return response.data;
  },
  delete: async (id: string) => {
    const response = await api.delete(`/contributions/${id}`);
    return response.data;
  },
};

// Projects API
export const projectsAPI = {
  getAll: async (params?: {
    search?: string;
    status?: string;
    page?: number;
    limit?: number;
  }) => {
    const response = await api.get('/projects', { params });
    return response.data;
  },
  getById: async (id: string) => {
    const response = await api.get(`/projects/${id}`);
    return response.data;
  },
  create: async (data: {
    name: string;
    description: string;
    target_amount: number;
    start_date: string;
    end_date: string;
    status: string;
  }) => {
    const response = await api.post('/projects', data);
    return response.data;
  },
  update: async (id: string, data: {
    name?: string;
    description?: string;
    target_amount?: number;
    start_date?: string;
    end_date?: string;
    status?: string;
  }) => {
    const response = await api.put(`/projects/${id}`, data);
    return response.data;
  },
  delete: async (id: string) => {
    const response = await api.delete(`/projects/${id}`);
    return response.data;
  },
};

// Groups API
export const groupsAPI = {
  getAll: async (params?: {
    search?: string;
    page?: number;
    limit?: number;
  }) => {
    const response = await api.get('/groups', { params });
    return response.data;
  },
  getById: async (id: string) => {
    const response = await api.get(`/groups/${id}`);
    return response.data;
  },
  create: async (data: {
    name: string;
    description: string;
    leader_id: string;
  }) => {
    const response = await api.post('/groups', data);
    return response.data;
  },
  update: async (id: string, data: {
    name?: string;
    description?: string;
    leader_id?: string;
  }) => {
    const response = await api.put(`/groups/${id}`, data);
    return response.data;
  },
  delete: async (id: string) => {
    const response = await api.delete(`/groups/${id}`);
    return response.data;
  },
};

// Reports API
export const reportsAPI = {
  getContributionReport: async (params?: {
    start_date?: string;
    end_date?: string;
    group_id?: string;
  }) => {
    const response = await api.get('/reports/contributions', { params });
    return response.data;
  },
  getMemberReport: async (params?: {
    group_id?: string;
    status?: string;
  }) => {
    const response = await api.get('/reports/members', { params });
    return response.data;
  },
  getProjectReport: async (params?: {
    status?: string;
    start_date?: string;
    end_date?: string;
  }) => {
    const response = await api.get('/reports/projects', { params });
    return response.data;
  },
};

// Settings API
export const settingsAPI = {
  getSettings: async () => {
    const response = await api.get('/settings');
    return response.data;
  },
  updateSettings: async (data: {
    organization_name?: string;
    organization_email?: string;
    organization_phone?: string;
    organization_address?: string;
    notification_preferences?: {
      email_notifications?: boolean;
      sms_notifications?: boolean;
      contribution_reminders?: boolean;
      project_updates?: boolean;
    };
  }) => {
    const response = await api.put('/settings', data);
    return response.data;
  },
  backupData: async () => {
    const response = await api.post('/settings/backup');
    return response.data;
  },
  restoreData: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/settings/restore', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
}; 