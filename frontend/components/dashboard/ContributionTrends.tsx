'use client';

import { Card, Title, AreaChart } from '@tremor/react';
import { format, subDays } from 'date-fns';

interface ContributionData {
  date: string;
  amount: number;
  count: number;
}

interface ContributionTrendsProps {
  data?: ContributionData[];
  isLoading?: boolean;
}

export function ContributionTrends({ data, isLoading }: ContributionTrendsProps) {
  // Generate mock data if none provided
  const chartData = data || Array.from({ length: 30 }, (_, i) => ({
    date: format(subDays(new Date(), 29 - i), 'MMM dd'),
    amount: Math.floor(Math.random() * 10000) + 1000,
    count: Math.floor(Math.random() * 20) + 5,
  }));

  return (
    <Card className="mt-4">
      <Title>Contribution Trends</Title>
      <AreaChart
        className="mt-4 h-72"
        data={chartData}
        index="date"
        categories={['amount', 'count']}
        colors={['indigo', 'cyan']}
        valueFormatter={(value) => {
          if (value >= 1000) {
            return `$${(value / 1000).toFixed(1)}k`;
          }
          return `$${value}`;
        }}
        yAxisWidth={60}
        showLegend
        showGridLines
        showAnimation
      />
    </Card>
  );
} 