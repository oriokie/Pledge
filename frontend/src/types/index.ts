export interface User {
  id: number;
  full_name: string;
  email: string;
  phone_number: string;
  role: 'admin' | 'staff' | 'member';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginCredentials {
  phone_number: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface Member {
  id: number;
  full_name: string;
  phone_number: string;
  email: string;
  phone: string | null;
  alias1: string | null;
  alias2: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Project {
  id: number;
  name: string;
  description: string;
  target_amount: number;
  status: 'active' | 'completed' | 'on_hold';
  start_date: string | null;
  end_date: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  description: string;
  target_amount: number;
  status: 'active' | 'completed' | 'on_hold';
  start_date: string | null;
  end_date: string | null;
  is_active: boolean;
}

export interface ProjectUpdate extends Partial<ProjectCreate> {}

export interface Contribution {
  id: number;
  member_id: number;
  project_id: number;
  amount: number;
  date: string;
  payment_method: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface Group {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface Notification {
  id: number;
  user_id: number;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  read: boolean;
  created_at: string;
  updated_at: string;
}

export interface File {
  id: number;
  name: string;
  path: string;
  type: string;
  size: number;
  uploaded_by: number;
  created_at: string;
  updated_at: string;
} 