import { NextResponse } from 'next/server';
import { contributions, pledges } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';

export async function POST(request: Request) {
  try {
    const { user } = useAuth();
    if (!user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const formData = await request.formData();
    const file = formData.get('file') as File;
    const type = formData.get('type') as string || 'all';

    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      );
    }

    const text = await file.text();
    const data = parseCSV(text);

    const results = {
      contributions: [],
      pledges: [],
      errors: [],
    };

    if (type === 'all' || type === 'contributions') {
      for (const contribution of data.contributions) {
        try {
          const result = await contributions.create({
            ...contribution,
            user_id: user.id,
          });
          results.contributions.push(result);
        } catch (error) {
          results.errors.push({
            type: 'contribution',
            data: contribution,
            error: error.message,
          });
        }
      }
    }

    if (type === 'all' || type === 'pledges') {
      for (const pledge of data.pledges) {
        try {
          const result = await pledges.create({
            ...pledge,
            user_id: user.id,
          });
          results.pledges.push(result);
        } catch (error) {
          results.errors.push({
            type: 'pledge',
            data: pledge,
            error: error.message,
          });
        }
      }
    }

    return NextResponse.json(results);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to import data' },
      { status: 500 }
    );
  }
}

function parseCSV(text: string): { contributions: any[]; pledges: any[] } {
  const lines = text.split('\n');
  const result = {
    contributions: [],
    pledges: [],
  };

  let currentSection = '';
  let headers: string[] = [];

  for (const line of lines) {
    if (!line.trim()) continue;

    if (line === 'Contributions') {
      currentSection = 'contributions';
      headers = [];
    } else if (line === 'Pledges') {
      currentSection = 'pledges';
      headers = [];
    } else if (!headers.length) {
      headers = line.split(',');
    } else {
      const values = line.split(',');
      const item: any = {};

      headers.forEach((header, index) => {
        const value = values[index];
        item[header.toLowerCase().replace(/\s+/g, '_')] = value;
      });

      if (currentSection === 'contributions') {
        result.contributions.push(item);
      } else if (currentSection === 'pledges') {
        result.pledges.push(item);
      }
    }
  }

  return result;
} 