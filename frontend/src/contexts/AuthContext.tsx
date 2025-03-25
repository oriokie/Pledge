'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { User } from '@/types';
import { login as apiLogin, logout as apiLogout, apiClient } from '@/lib/api';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (phone_number: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Set default auth header
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      // For now, create a temporary user object
      setUser({ id: 1, full_name: 'User', phone_number: '', role: 'admin' });
      setLoading(false);
    } else {
      setLoading(false);
      router.push('/login');
    }
  }, [router]);

  const login = async (phone_number: string, password: string) => {
    try {
      const response = await apiLogin(phone_number, password);
      localStorage.setItem('token', response.access_token);
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.access_token}`;
      // For now, create a temporary user object
      setUser({ id: 1, full_name: 'User', phone_number: phone_number, role: 'admin' });
      router.push('/dashboard');
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await apiLogout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
      delete apiClient.defaults.headers.common['Authorization'];
      setUser(null);
      router.push('/login');
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
} 