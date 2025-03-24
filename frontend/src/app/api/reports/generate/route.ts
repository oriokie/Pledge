import { NextResponse } from 'next/server';
import { reports } from '@/lib/api';

export async function POST(request: Request) {
  try {
    const { report_type, parameters } = await request.json();
    const data = await reports.generate(report_type, parameters);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to generate report' },
      { status: 500 }
    );
  }
} 