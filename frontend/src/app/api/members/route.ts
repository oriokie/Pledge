import { NextResponse } from 'next/server';
import { members } from '@/lib/api';

export async function GET() {
  try {
    const data = await members.getAll();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get members' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const data = await members.create(body);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create member' },
      { status: 500 }
    );
  }
} 