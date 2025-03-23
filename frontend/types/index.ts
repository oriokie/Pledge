export interface Member {
  id: number;
  name: string;
  phone: string;
  alias: string;
  active: boolean;
  uniqueCode: string;
  createdAt: string;
  updatedAt: string;
}

export interface Contribution {
  id: number;
  memberId: number;
  projectId: number;
  groupId?: number;
  amount: number;
  status: 'pending' | 'completed';
  date: string;
  createdAt: string;
  updatedAt: string;
}

export interface Project {
  id: number;
  name: string;
  description: string;
  targetAmount: number;
  currentAmount: number;
  members: number;
  status: 'active' | 'completed';
  startDate: string;
  endDate: string;
  createdAt: string;
  updatedAt: string;
}

export interface Group {
  id: number;
  name: string;
  description: string;
  memberCount: number;
  createdAt: string;
  updatedAt: string;
}

export interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user';
  active: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
} 