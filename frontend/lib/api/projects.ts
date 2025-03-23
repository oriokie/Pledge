export interface Project {
  id: string;
  name: string;
  description: string;
  startDate: string;
  endDate?: string;
  status: 'planned' | 'in_progress' | 'completed' | 'on_hold';
  target: number;
  raised: number;
  contributors: number;
  groupId?: string;
  category: 'building' | 'missions' | 'outreach' | 'equipment' | 'other';
  milestones?: {
    total: number;
    completed: number;
  };
}

export interface ProjectCreateInput {
  name: string;
  description: string;
  startDate: string;
  endDate?: string;
  target: number;
  category: Project['category'];
  groupId?: string;
}

export interface ProjectUpdateInput extends Partial<ProjectCreateInput> {
  id: string;
  status?: Project['status'];
  raised?: number;
}

export interface ProjectFilters {
  status?: Project['status'];
  category?: Project['category'];
  groupId?: string;
  search?: string;
  startDateFrom?: string;
  startDateTo?: string;
  endDateFrom?: string;
  endDateTo?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || 'An error occurred while fetching data');
  }
  return response.json();
}

export async function getProjects(filters?: ProjectFilters): Promise<Project[]> {
  const queryParams = new URLSearchParams();
  if (filters) {
    Object.entries(filters).forEach(([key, value]) => {
      if (value) queryParams.append(key, value);
    });
  }

  const response = await fetch(
    `${API_BASE_URL}/api/projects?${queryParams.toString()}`,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  return handleResponse<Project[]>(response);
}

export async function getProjectById(id: string): Promise<Project> {
  const response = await fetch(`${API_BASE_URL}/api/projects/${id}`, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return handleResponse<Project>(response);
}

export async function createProject(data: ProjectCreateInput): Promise<Project> {
  const response = await fetch(`${API_BASE_URL}/api/projects`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  return handleResponse<Project>(response);
}

export async function updateProject(data: ProjectUpdateInput): Promise<Project> {
  const response = await fetch(`${API_BASE_URL}/api/projects/${data.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  return handleResponse<Project>(response);
}

export async function deleteProject(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/projects/${id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return handleResponse<void>(response);
}

export async function getProjectStats(
  startDate?: string,
  endDate?: string
): Promise<{
  totalProjects: number;
  activeProjects: number;
  totalRaised: number;
  totalTarget: number;
  byCategory: Record<Project['category'], number>;
  byStatus: Record<Project['status'], number>;
  completionRate: number;
}> {
  const queryParams = new URLSearchParams();
  if (startDate) queryParams.append('startDate', startDate);
  if (endDate) queryParams.append('endDate', endDate);

  const response = await fetch(
    `${API_BASE_URL}/api/projects/stats?${queryParams.toString()}`,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  return handleResponse<{
    totalProjects: number;
    activeProjects: number;
    totalRaised: number;
    totalTarget: number;
    byCategory: Record<Project['category'], number>;
    byStatus: Record<Project['status'], number>;
    completionRate: number;
  }>(response);
}

export async function addContribution(
  projectId: string,
  data: {
    memberId: string;
    amount: number;
    date: string;
  }
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/api/projects/${projectId}/contributions`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }
  );

  return handleResponse<void>(response);
}

export async function updateMilestones(
  projectId: string,
  data: {
    total: number;
    completed: number;
  }
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/api/projects/${projectId}/milestones`,
    {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }
  );

  return handleResponse<void>(response);
} 