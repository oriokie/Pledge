import { Member } from '@/types';
import { apiClient } from './index';

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