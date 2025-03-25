import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { User, LoginCredentials, Token } from '@/types';
import { login as loginApi } from '@/lib/api/auth';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');
    if (token && userStr) {
      try {
        setUser(JSON.parse(userStr));
      } catch (error) {
        console.error('Error parsing user data:', error);
      }
    }
    setLoading(false);
  }, []);

  const login = async (credentials: LoginCredentials) => {
    try {
      const response = await loginApi(credentials);
      const { access_token, token_type } = response;
      const token = `${token_type} ${access_token}`;
      
      // Store token and user data
      localStorage.setItem('token', token);
      
      // Get user data from the response
      const userData = response.user as User;
      localStorage.setItem('user', JSON.stringify(userData));
      
      setUser(userData);
      router.push('/dashboard');
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    router.push('/login');
  };

  return {
    user,
    loading,
    login,
    logout,
  };
} 