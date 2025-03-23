export interface Contribution {
  id: string;
  memberId: string;
  memberName: string;
  amount: number;
  type: 'tithe' | 'offering' | 'special' | 'project';
  project?: string;
  date: string;
  status: 'pending' | 'completed' | 'failed';
  paymentMethod: 'cash' | 'check' | 'card' | 'bank_transfer';
  notes?: string;
}

export interface ContributionCreateInput {
  memberId: string;
  amount: number;
  type: Contribution['type'];
  project?: string;
  paymentMethod: Contribution['paymentMethod'];
  notes?: string;
}

export interface ContributionUpdateInput extends Partial<ContributionCreateInput> {
  id: string;
  status?: Contribution['status'];
}

export interface ContributionFilters {
  memberId?: string;
  type?: Contribution['type'];
  status?: Contribution['status'];
  startDate?: string;
  endDate?: string;
  project?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || 'An error occurred while fetching data');
  }
  return response.json();
}

export async function getContributions(filters?: ContributionFilters): Promise<Contribution[]> {
  const queryParams = new URLSearchParams();
  if (filters) {
    Object.entries(filters).forEach(([key, value]) => {
      if (value) queryParams.append(key, value);
    });
  }

  const response = await fetch(
    `${API_BASE_URL}/api/contributions?${queryParams.toString()}`,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  return handleResponse<Contribution[]>(response);
}

export async function getContributionById(id: string): Promise<Contribution> {
  const response = await fetch(`${API_BASE_URL}/api/contributions/${id}`, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return handleResponse<Contribution>(response);
}

export async function createContribution(
  data: ContributionCreateInput
): Promise<Contribution> {
  const response = await fetch(`${API_BASE_URL}/api/contributions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  return handleResponse<Contribution>(response);
}

export async function updateContribution(
  data: ContributionUpdateInput
): Promise<Contribution> {
  const response = await fetch(`${API_BASE_URL}/api/contributions/${data.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  return handleResponse<Contribution>(response);
}

export async function deleteContribution(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/contributions/${id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return handleResponse<void>(response);
}

export async function getContributionStats(
  startDate?: string,
  endDate?: string
): Promise<{
  totalAmount: number;
  contributionCount: number;
  averageAmount: number;
  byType: Record<Contribution['type'], number>;
}> {
  const queryParams = new URLSearchParams();
  if (startDate) queryParams.append('startDate', startDate);
  if (endDate) queryParams.append('endDate', endDate);

  const response = await fetch(
    `${API_BASE_URL}/api/contributions/stats?${queryParams.toString()}`,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  return handleResponse<{
    totalAmount: number;
    contributionCount: number;
    averageAmount: number;
    byType: Record<Contribution['type'], number>;
  }>(response);
}

export async function getContributionTrends(
  days: number = 30
): Promise<Array<{ date: string; amount: number; count: number }>> {
  const response = await fetch(
    `${API_BASE_URL}/api/contributions/trends?days=${days}`,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  return handleResponse<Array<{ date: string; amount: number; count: number }>>(
    response
  );
} 