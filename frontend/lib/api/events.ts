export interface Event {
  id: string;
  title: string;
  description?: string;
  date: string;
  endDate?: string;
  location: string;
  type: 'meeting' | 'service' | 'event';
  status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled';
  attendees: {
    expected: number;
    confirmed?: number;
  };
  groupId?: string;
  recurringId?: string;
  isRecurring: boolean;
}

export interface EventCreateInput {
  title: string;
  description?: string;
  date: string;
  endDate?: string;
  location: string;
  type: Event['type'];
  attendees: {
    expected: number;
  };
  groupId?: string;
  isRecurring?: boolean;
  recurrence?: {
    frequency: 'daily' | 'weekly' | 'monthly';
    endDate: string;
  };
}

export interface EventUpdateInput extends Partial<EventCreateInput> {
  id: string;
  status?: Event['status'];
}

export interface EventFilters {
  type?: Event['type'];
  status?: Event['status'];
  groupId?: string;
  startDate?: string;
  endDate?: string;
  search?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || 'An error occurred while fetching data');
  }
  return response.json();
}

export async function getEvents(filters?: EventFilters): Promise<Event[]> {
  const queryParams = new URLSearchParams();
  if (filters) {
    Object.entries(filters).forEach(([key, value]) => {
      if (value) queryParams.append(key, value);
    });
  }

  const response = await fetch(
    `${API_BASE_URL}/api/events?${queryParams.toString()}`,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  return handleResponse<Event[]>(response);
}

export async function getEventById(id: string): Promise<Event> {
  const response = await fetch(`${API_BASE_URL}/api/events/${id}`, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return handleResponse<Event>(response);
}

export async function createEvent(data: EventCreateInput): Promise<Event> {
  const response = await fetch(`${API_BASE_URL}/api/events`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  return handleResponse<Event>(response);
}

export async function updateEvent(data: EventUpdateInput): Promise<Event> {
  const response = await fetch(`${API_BASE_URL}/api/events/${data.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  return handleResponse<Event>(response);
}

export async function deleteEvent(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/events/${id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return handleResponse<void>(response);
}

export async function getEventStats(
  startDate?: string,
  endDate?: string
): Promise<{
  totalEvents: number;
  upcomingEvents: number;
  averageAttendance: number;
  byType: Record<Event['type'], number>;
}> {
  const queryParams = new URLSearchParams();
  if (startDate) queryParams.append('startDate', startDate);
  if (endDate) queryParams.append('endDate', endDate);

  const response = await fetch(
    `${API_BASE_URL}/api/events/stats?${queryParams.toString()}`,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  return handleResponse<{
    totalEvents: number;
    upcomingEvents: number;
    averageAttendance: number;
    byType: Record<Event['type'], number>;
  }>(response);
}

export async function getUpcomingEvents(limit: number = 5): Promise<Event[]> {
  const response = await fetch(
    `${API_BASE_URL}/api/events/upcoming?limit=${limit}`,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  return handleResponse<Event[]>(response);
}

export async function confirmAttendance(
  eventId: string,
  memberId: string
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/api/events/${eventId}/attendance/${memberId}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  return handleResponse<void>(response);
} 