'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { User } from '@/types';
import { auth } from '@/lib/api';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (phone: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    checkUser();
  }, []);

  const checkUser = async () => {
    try {
      const currentUser = await auth.getCurrentUser();
      setUser(currentUser);
      setError(null);
    } catch (err) {
      setUser(null);
      setError('Failed to fetch user');
    } finally {
      setLoading(false);
    }
  };

  const login = async (phone: string, password: string) => {
    try {
      setLoading(true);
      const { access_token } = await auth.login({ phone, password });
      localStorage.setItem('token', access_token);
      await checkUser();
    } catch (err) {
      setError('Invalid credentials');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, error, login, logout }}>
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