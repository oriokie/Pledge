import { NextResponse } from 'next/server';
import { pledges } from '@/lib/api';

export async function GET() {
  try {
    const data = await pledges.getAll();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get pledges' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const data = await pledges.create(body);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create pledge' },
      { status: 500 }
    );
  }
} 