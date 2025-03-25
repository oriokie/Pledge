import { Project, ProjectCreate, ProjectUpdate } from '@/types';
import { apiClient } from './index';

export const getProjects = async (): Promise<Project[]> => {
  const response = await apiClient.get('/projects');
  return response.data;
};

export const createProject = async (data: ProjectCreate): Promise<Project> => {
  const response = await apiClient.post('/projects', data);
  return response.data;
};

export const updateProject = async (id: number, data: ProjectUpdate): Promise<Project> => {
  const response = await apiClient.put(`/projects/${id}`, data);
  return response.data;
};

export const deleteProject = async (id: number): Promise<void> => {
  await apiClient.delete(`/projects/${id}`);
}; 