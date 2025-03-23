'use client';

import { Card, Title, BarList, Bold, Flex, Text } from '@tremor/react';
import { Project } from '@/lib/api/projects';

interface ProjectProgressProps {
  data?: Project[];
  isLoading?: boolean;
}

export function ProjectProgress({ data, isLoading }: ProjectProgressProps) {
  // Mock data if none provided
  const projects = data || [
    {
      id: '1',
      name: 'Building Renovation',
      description: 'Church building renovation project',
      startDate: '2024-01-01',
      status: 'in_progress',
      target: 100000,
      raised: 65000,
      contributors: 45,
      category: 'building',
      milestones: {
        total: 10,
        completed: 6,
      },
    },
    {
      id: '2',
      name: 'Mission Trip',
      description: 'Summer mission trip to South America',
      startDate: '2024-03-01',
      status: 'in_progress',
      target: 25000,
      raised: 15000,
      contributors: 30,
      category: 'missions',
      milestones: {
        total: 5,
        completed: 2,
      },
    },
    {
      id: '3',
      name: 'Youth Center Equipment',
      description: 'New equipment for youth center',
      startDate: '2024-02-15',
      status: 'in_progress',
      target: 15000,
      raised: 12000,
      contributors: 25,
      category: 'equipment',
      milestones: {
        total: 8,
        completed: 5,
      },
    },
  ] as Project[];

  const progressData = projects
    .filter((project) => project.status === 'in_progress')
    .map((project) => ({
      name: project.name,
      value: project.raised,
      target: project.target,
      progress: Math.round((project.raised / project.target) * 100),
      milestoneProgress: Math.round(
        ((project.milestones?.completed || 0) /
          (project.milestones?.total || 1)) *
          100
      ),
    }))
    .sort((a, b) => b.progress - a.progress);

  if (isLoading) {
    return (
      <Card className="mt-4">
        <Title>Project Progress</Title>
        <div className="mt-4 space-y-4">
          {[...Array(3)].map((_, i) => (
            <div
              key={i}
              className="animate-pulse space-y-2"
            >
              <div className="h-4 w-1/3 rounded bg-gray-200 dark:bg-gray-700" />
              <div className="h-3 w-full rounded bg-gray-200 dark:bg-gray-700" />
              <div className="flex justify-between">
                <div className="h-3 w-16 rounded bg-gray-200 dark:bg-gray-700" />
                <div className="h-3 w-16 rounded bg-gray-200 dark:bg-gray-700" />
              </div>
            </div>
          ))}
        </div>
      </Card>
    );
  }

  return (
    <Card className="mt-4">
      <Title>Project Progress</Title>
      <div className="mt-4 space-y-6">
        {progressData.map((project) => (
          <div key={project.name} className="space-y-2">
            <Flex>
              <Text>{project.name}</Text>
              <Text>
                {new Intl.NumberFormat('en-US', {
                  style: 'currency',
                  currency: 'USD',
                }).format(project.value)}{' '}
                /{' '}
                {new Intl.NumberFormat('en-US', {
                  style: 'currency',
                  currency: 'USD',
                }).format(project.target)}
              </Text>
            </Flex>
            <div className="h-2 w-full rounded-full bg-gray-200 dark:bg-gray-700">
              <div
                className="h-2 rounded-full bg-indigo-600 transition-all duration-500 dark:bg-indigo-400"
                style={{ width: `${project.progress}%` }}
              />
            </div>
            <Flex className="text-sm">
              <Text>Fundraising: {project.progress}%</Text>
              <Text>Milestones: {project.milestoneProgress}%</Text>
            </Flex>
          </div>
        ))}
      </div>
    </Card>
  );
} 