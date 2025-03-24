import { NextResponse } from 'next/server';
import { contributions, pledges } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';

export async function GET() {
  try {
    const { user } = useAuth();
    if (!user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Get user's contributions and pledges
    const [contributionsData, pledgesData] = await Promise.all([
      contributions.getAll(),
      pledges.getAll(),
    ]);

    const userContributions = contributionsData.filter(
      (contribution) => contribution.user_id === user.id
    );
    const userPledges = pledgesData.filter(
      (pledge) => pledge.user_id === user.id
    );

    // Calculate statistics
    const totalContributions = userContributions.reduce(
      (sum, contribution) => sum + contribution.amount,
      0
    );
    const totalPledges = userPledges.reduce(
      (sum, pledge) => sum + pledge.amount,
      0
    );
    const pendingPledges = userPledges
      .filter((pledge) => pledge.status === 'PENDING')
      .reduce((sum, pledge) => sum + pledge.amount, 0);
    const paidPledges = userPledges
      .filter((pledge) => pledge.status === 'PAID')
      .reduce((sum, pledge) => sum + pledge.amount, 0);

    // Calculate monthly statistics
    const monthlyContributions = userContributions.reduce((acc, contribution) => {
      const month = new Date(contribution.created_at).toISOString().slice(0, 7);
      acc[month] = (acc[month] || 0) + contribution.amount;
      return acc;
    }, {} as Record<string, number>);

    const monthlyPledges = userPledges.reduce((acc, pledge) => {
      const month = new Date(pledge.created_at).toISOString().slice(0, 7);
      acc[month] = (acc[month] || 0) + pledge.amount;
      return acc;
    }, {} as Record<string, number>);

    // Calculate pledge status distribution
    const pledgeStatusDistribution = userPledges.reduce((acc, pledge) => {
      acc[pledge.status] = (acc[pledge.status] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    return NextResponse.json({
      totalContributions,
      totalPledges,
      pendingPledges,
      paidPledges,
      monthlyContributions,
      monthlyPledges,
      pledgeStatusDistribution,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get statistics' },
      { status: 500 }
    );
  }
} 