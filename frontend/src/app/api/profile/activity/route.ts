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

    // Format activity logs
    const activityLogs = [
      ...userContributions.map((contribution) => ({
        type: 'contribution',
        id: contribution.id,
        amount: contribution.amount,
        description: contribution.description,
        created_at: contribution.created_at,
      })),
      ...userPledges.map((pledge) => ({
        type: 'pledge',
        id: pledge.id,
        amount: pledge.amount,
        description: pledge.description,
        status: pledge.status,
        due_date: pledge.due_date,
        created_at: pledge.created_at,
      })),
    ].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());

    return NextResponse.json(activityLogs);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get activity logs' },
      { status: 500 }
    );
  }
} 