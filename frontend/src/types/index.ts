export interface User {
  id: number;
  email: string;
  phone: string;
  full_name: string;
  role: 'ADMIN' | 'STAFF' | 'MEMBER';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Member {
  id: number;
  name: string;
  phone_number: string;
  email: string;
  created_by_user_id: number;
  created_at: string;
  updated_at: string;
}

export interface Group {
  id: number;
  name: string;
  description: string;
  created_by_user_id: number;
  created_at: string;
  updated_at: string;
  members: Member[];
}

export interface Project {
  id: number;
  name: string;
  description: string;
  start_date: string;
  end_date: string;
  status: 'PLANNED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';
  created_by_user_id: number;
  created_at: string;
  updated_at: string;
}

export interface File {
  id: number;
  name: string;
  file_path: string;
  file_type: string;
  file_size: number;
  uploaded_by_user_id: number;
  created_at: string;
  updated_at: string;
}

export interface Report {
  id: number;
  title: string;
  description: string;
  report_type: 'CONTRIBUTION' | 'PLEDGE' | 'MEMBER' | 'GROUP' | 'PROJECT';
  parameters: Record<string, any>;
  file_id?: number;
  created_by_user_id: number;
  created_at: string;
  updated_at: string;
  file?: File;
}

export interface PasswordUpdate {
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface Contribution {
  id: number;
  user_id: number;
  amount: number;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface Pledge {
  id: number;
  user_id: number;
  amount: number;
  description: string;
  status: 'PENDING' | 'PAID' | 'CANCELLED';
  due_date: string;
  created_at: string;
  updated_at: string;
} 