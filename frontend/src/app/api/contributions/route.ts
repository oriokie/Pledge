import { NextResponse } from 'next/server';
import { contributions } from '@/lib/api';

export async function GET() {
  try {
    const data = await contributions.getAll();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get contributions' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const data = await contributions.create(body);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create contribution' },
      { status: 500 }
    );
  }
} 