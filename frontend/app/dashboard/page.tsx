'use client';

import { useState, useEffect } from 'react';
import { ContributionTrends } from '@/components/dashboard/ContributionTrends';
import { MemberDistribution } from '@/components/dashboard/MemberDistribution';
import { TopContributors } from '@/components/dashboard/TopContributors';
import { UpcomingEvents } from '@/components/dashboard/UpcomingEvents';
import { DashboardCustomizer, WidgetConfig } from '@/components/dashboard/DashboardCustomizer';
import { DateRangeSelector } from '@/components/dashboard/DateRangeSelector';
import { useApiQuery } from '@/lib/hooks/useApiQuery';
import { useToast } from '@/contexts/ToastContext';
import { cn } from '@/lib/utils';
import { getContributionStats } from '@/lib/api/contributions';
import { getMemberStats } from '@/lib/api/members';
import { getUpcomingEvents } from '@/lib/api/events';
import { format } from 'date-fns';

const defaultWidgets: WidgetConfig[] = [
  { id: 'contribution-trends', title: 'Contribution Trends', type: 'chart', size: 'large', visible: true },
  { id: 'member-distribution', title: 'Member Distribution', type: 'chart', size: 'medium', visible: true },
  { id: 'top-contributors', title: 'Top Contributors', type: 'list', size: 'medium', visible: true },
  { id: 'upcoming-events', title: 'Upcoming Events', type: 'list', size: 'small', visible: true },
];

interface DateRange {
  start: Date;
  end: Date;
}

export default function DashboardPage() {
  const [dateRange, setDateRange] = useState<DateRange>({
    start: new Date(new Date().setDate(new Date().getDate() - 30)),
    end: new Date(),
  });
  const [widgets, setWidgets] = useState<WidgetConfig[]>(() => {
    const savedWidgets = localStorage.getItem('dashboard-widgets');
    return savedWidgets ? JSON.parse(savedWidgets) : defaultWidgets;
  });
  const { showToast } = useToast();

  // Save widget configuration to localStorage
  useEffect(() => {
    localStorage.setItem('dashboard-widgets', JSON.stringify(widgets));
  }, [widgets]);

  // Format dates for API calls
  const startDateStr = format(dateRange.start, 'yyyy-MM-dd');
  const endDateStr = format(dateRange.end, 'yyyy-MM-dd');

  // Fetch data using React Query
  const { data: contributionData, isLoading: isLoadingContributions } = useApiQuery({
    queryKey: ['contributions', startDateStr, endDateStr],
    queryFn: () => getContributionStats(startDateStr, endDateStr),
  });

  const { data: memberData, isLoading: isLoadingMembers } = useApiQuery({
    queryKey: ['members'],
    queryFn: getMemberStats,
  });

  const { data: eventData, isLoading: isLoadingEvents } = useApiQuery({
    queryKey: ['events'],
    queryFn: getUpcomingEvents,
  });

  const handleWidgetsChange = (newWidgets: WidgetConfig[]) => {
    setWidgets(newWidgets);
    showToast('Dashboard layout updated successfully', 'success');
  };

  const getWidgetSizeClass = (size: 'small' | 'medium' | 'large') => {
    switch (size) {
      case 'small':
        return 'col-span-1';
      case 'medium':
        return 'col-span-2';
      case 'large':
        return 'col-span-3';
      default:
        return 'col-span-1';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <div className="flex items-center space-x-4">
          <DateRangeSelector
            onChange={(range: DateRange) => setDateRange(range)}
            className="w-64"
          />
          <DashboardCustomizer
            widgets={widgets}
            onWidgetsChange={handleWidgetsChange}
          />
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {widgets.map((widget) => {
          if (!widget.visible) return null;

          return (
            <div
              key={widget.id}
              className={cn(
                'rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800',
                getWidgetSizeClass(widget.size)
              )}
            >
              <h2 className="mb-4 text-lg font-medium">{widget.title}</h2>
              {widget.id === 'contribution-trends' && (
                <ContributionTrends
                  data={contributionData?.trends || []}
                  isLoading={isLoadingContributions}
                />
              )}
              {widget.id === 'member-distribution' && (
                <MemberDistribution
                  data={memberData?.membersByGroup || {}}
                  isLoading={isLoadingMembers}
                />
              )}
              {widget.id === 'top-contributors' && (
                <TopContributors
                  data={contributionData?.topContributors || []}
                  isLoading={isLoadingContributions}
                />
              )}
              {widget.id === 'upcoming-events' && (
                <UpcomingEvents
                  events={eventData || []}
                  isLoading={isLoadingEvents}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
} 