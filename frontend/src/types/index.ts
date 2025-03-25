export interface User {
  id: number;
  full_name: string;
  phone_number: string;
  role: 'ADMIN' | 'STAFF';
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
  phone: string | null;
  email: string | null;
  member_code: string;
  alias1: string | null;
  alias2: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  created_by_id: number;
  total_contributions?: number;
  total_pledges?: number;
  group_names?: string[];
} 