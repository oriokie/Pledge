import { NextResponse } from 'next/server';
import { groups } from '@/lib/api';

export async function GET() {
  try {
    const data = await groups.getAll();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get groups' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const data = await groups.create(body);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create group' },
      { status: 500 }
    );
  }
} 