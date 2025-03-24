import { NextResponse } from 'next/server';
import { users, contributions, pledges } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';

export async function GET(request: Request) {
  try {
    const { user } = useAuth();
    if (!user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const { searchParams } = new URL(request.url);
    const query = searchParams.get('q') || '';
    const type = searchParams.get('type') || 'all';

    if (!query) {
      return NextResponse.json({ results: [] });
    }

    let results: Array<{
      type: string;
      id: number;
      title: string;
      subtitle: string;
      description: string;
    }> = [];

    if (type === 'all' || type === 'users') {
      const usersData = await users.getAll();
      const userResults = usersData
        .filter((u) => {
          const searchString = `${u.full_name} ${u.email} ${u.phone}`.toLowerCase();
          return searchString.includes(query.toLowerCase());
        })
        .map((u) => ({
          type: 'user',
          id: u.id,
          title: u.full_name,
          subtitle: u.email,
          description: u.phone,
        }));
      results = [...results, ...userResults];
    }

    if (type === 'all' || type === 'contributions') {
      const contributionsData = await contributions.getAll();
      const contributionResults = contributionsData
        .filter((c) => {
          const searchString = `${c.description} ${c.amount}`.toLowerCase();
          return searchString.includes(query.toLowerCase());
        })
        .map((c) => ({
          type: 'contribution',
          id: c.id,
          title: c.description,
          subtitle: `Amount: ${c.amount}`,
          description: new Date(c.created_at).toLocaleDateString(),
        }));
      results = [...results, ...contributionResults];
    }

    if (type === 'all' || type === 'pledges') {
      const pledgesData = await pledges.getAll();
      const pledgeResults = pledgesData
        .filter((p) => {
          const searchString = `${p.description} ${p.amount} ${p.status}`.toLowerCase();
          return searchString.includes(query.toLowerCase());
        })
        .map((p) => ({
          type: 'pledge',
          id: p.id,
          title: p.description,
          subtitle: `Amount: ${p.amount}`,
          description: `Status: ${p.status}`,
        }));
      results = [...results, ...pledgeResults];
    }

    return NextResponse.json({ results });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to perform search' },
      { status: 500 }
    );
  }
} 