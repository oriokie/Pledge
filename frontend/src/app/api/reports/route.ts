import { NextResponse } from 'next/server';
import { reports } from '@/lib/api';

export async function GET() {
  try {
    const data = await reports.getAll();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch reports' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const data = await reports.create(body);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create report' },
      { status: 500 }
    );
  }
} 