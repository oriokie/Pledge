import { NextResponse } from 'next/server';
import { contributions, pledges } from '@/lib/api';
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
    const type = searchParams.get('type') || 'all';
    const format = searchParams.get('format') || 'json';

    let data: Record<string, any> = {};

    if (type === 'all' || type === 'contributions') {
      const contributionsData = await contributions.getAll();
      const userContributions = contributionsData.filter(
        (contribution) => contribution.user_id === user.id
      );
      data = {
        ...data,
        contributions: userContributions,
      };
    }

    if (type === 'all' || type === 'pledges') {
      const pledgesData = await pledges.getAll();
      const userPledges = pledgesData.filter(
        (pledge) => pledge.user_id === user.id
      );
      data = {
        ...data,
        pledges: userPledges,
      };
    }

    if (format === 'csv') {
      const csv = convertToCSV(data);
      return new NextResponse(csv, {
        headers: {
          'Content-Type': 'text/csv',
          'Content-Disposition': `attachment; filename="export-${type}-${new Date().toISOString()}.csv"`,
        },
      });
    }

    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to export data' },
      { status: 500 }
    );
  }
}

function convertToCSV(data: Record<string, any>): string {
  const rows: string[] = [];

  if (data.contributions) {
    rows.push('Contributions');
    rows.push('ID,Amount,Description,Created At');
    data.contributions.forEach((contribution: any) => {
      rows.push(
        `${contribution.id},${contribution.amount},${contribution.description},${contribution.created_at}`
      );
    });
    rows.push('');
  }

  if (data.pledges) {
    rows.push('Pledges');
    rows.push('ID,Amount,Description,Status,Due Date,Created At');
    data.pledges.forEach((pledge: any) => {
      rows.push(
        `${pledge.id},${pledge.amount},${pledge.description},${pledge.status},${pledge.due_date},${pledge.created_at}`
      );
    });
  }

  return rows.join('\n');
} 