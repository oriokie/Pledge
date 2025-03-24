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

    return NextResponse.json({
      totalContributions,
      totalPledges,
      pendingPledges,
      paidPledges,
      contributions: userContributions,
      pledges: userPledges,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get reports' },
      { status: 500 }
    );
  }
} 