'use client';

import { Card, Title, DonutChart, Legend } from '@tremor/react';

interface MemberStats {
  group: string;
  count: number;
}

interface MemberDistributionProps {
  data?: MemberStats[];
  isLoading?: boolean;
}

export function MemberDistribution({ data, isLoading }: MemberDistributionProps) {
  // Mock data if none provided
  const chartData = data || [
    { group: 'Youth Group', count: 45 },
    { group: 'Adult Ministry', count: 80 },
    { group: 'Worship Team', count: 25 },
    { group: 'Outreach', count: 30 },
    { group: 'Leadership', count: 15 },
  ];

  const colors = [
    'indigo',
    'cyan',
    'violet',
    'amber',
    'rose',
    'emerald',
    'slate',
  ];

  return (
    <Card className="mt-4">
      <Title>Member Distribution</Title>
      <div className="mt-4">
        <DonutChart
          className="mt-6 h-40"
          data={chartData}
          category="count"
          index="group"
          colors={colors}
          showAnimation
        />
        <Legend
          className="mt-6"
          categories={chartData.map((item) => item.group)}
          colors={colors}
        />
      </div>
    </Card>
  );
} 