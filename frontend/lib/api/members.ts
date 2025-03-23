export interface Member {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  address?: string;
  joinDate: string;
  status: 'active' | 'inactive' | 'pending';
  groups: string[];
  contributions?: {
    total: number;
    count: number;
    lastContribution?: string;
  };
}

export interface MemberCreateInput {
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  address?: string;
  groups?: string[];
}

export interface MemberUpdateInput extends Partial<MemberCreateInput> {
  id: string;
  status?: Member['status'];
}

export interface MemberFilters {
  status?: Member['status'];
  group?: string;
  search?: string;
  joinDateStart?: string;
  joinDateEnd?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || 'An error occurred while fetching data');
  }
  return response.json();
}

export async function getMembers(filters?: MemberFilters): Promise<Member[]> {
  const queryParams = new URLSearchParams();
  if (filters) {
    Object.entries(filters).forEach(([key, value]) => {
      if (value) queryParams.append(key, value);
    });
  }

  const response = await fetch(
    `${API_BASE_URL}/api/members?${queryParams.toString()}`,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  return handleResponse<Member[]>(response);
}

export async function getMemberById(id: string): Promise<Member> {
  const response = await fetch(`${API_BASE_URL}/api/members/${id}`, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return handleResponse<Member>(response);
}

export async function createMember(data: MemberCreateInput): Promise<Member> {
  const response = await fetch(`${API_BASE_URL}/api/members`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  return handleResponse<Member>(response);
}

export async function updateMember(data: MemberUpdateInput): Promise<Member> {
  const response = await fetch(`${API_BASE_URL}/api/members/${data.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  return handleResponse<Member>(response);
}

export async function deleteMember(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/members/${id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return handleResponse<void>(response);
}

export async function getMemberStats(): Promise<{
  totalMembers: number;
  activeMembers: number;
  newMembersThisMonth: number;
  membersByGroup: Record<string, number>;
  memberGrowth: number;
}> {
  const response = await fetch(`${API_BASE_URL}/api/members/stats`, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return handleResponse<{
    totalMembers: number;
    activeMembers: number;
    newMembersThisMonth: number;
    membersByGroup: Record<string, number>;
    memberGrowth: number;
  }>(response);
}

export async function assignMemberToGroup(
  memberId: string,
  groupId: string
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/api/members/${memberId}/groups/${groupId}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  return handleResponse<void>(response);
}

export async function removeMemberFromGroup(
  memberId: string,
  groupId: string
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/api/members/${memberId}/groups/${groupId}`,
    {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  return handleResponse<void>(response);
} 