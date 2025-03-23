'use client';

import { Card, Title } from '@tremor/react';
import { CalendarIcon, MapPinIcon, UserGroupIcon } from '@heroicons/react/24/outline';
import { format } from 'date-fns';

interface Event {
  id: string;
  title: string;
  date: Date;
  location: string;
  attendees: number;
  type: 'meeting' | 'service' | 'event';
}

interface UpcomingEventsProps {
  events?: Event[];
  isLoading?: boolean;
}

export function UpcomingEvents({ events, isLoading }: UpcomingEventsProps) {
  // Mock data if none provided
  const eventsList = events || [
    {
      id: '1',
      title: 'Sunday Service',
      date: new Date(new Date().setDate(new Date().getDate() + 2)),
      location: 'Main Sanctuary',
      attendees: 150,
      type: 'service',
    },
    {
      id: '2',
      title: 'Youth Group Meeting',
      date: new Date(new Date().setDate(new Date().getDate() + 3)),
      location: 'Youth Center',
      attendees: 45,
      type: 'meeting',
    },
    {
      id: '3',
      title: 'Community Outreach',
      date: new Date(new Date().setDate(new Date().getDate() + 5)),
      location: 'Community Center',
      attendees: 30,
      type: 'event',
    },
  ];

  return (
    <Card className="mt-4">
      <Title>Upcoming Events</Title>
      <div className="mt-4 space-y-4">
        {eventsList.map((event) => (
          <div
            key={event.id}
            className="flex items-start space-x-4 rounded-lg border p-4 hover:bg-gray-50 dark:hover:bg-gray-800"
          >
            <div className="flex-shrink-0">
              <CalendarIcon className="h-6 w-6 text-gray-400" />
            </div>
            <div className="min-w-0 flex-1">
              <div className="text-sm font-medium text-gray-900 dark:text-white">
                {event.title}
              </div>
              <div className="mt-1 flex items-center space-x-2 text-sm text-gray-500">
                <span>{format(event.date, 'MMM dd, yyyy')}</span>
                <span>•</span>
                <span>{format(event.date, 'h:mm a')}</span>
              </div>
              <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                <div className="flex items-center">
                  <MapPinIcon className="mr-1 h-4 w-4" />
                  {event.location}
                </div>
                <div className="flex items-center">
                  <UserGroupIcon className="mr-1 h-4 w-4" />
                  {event.attendees} attendees
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
} 