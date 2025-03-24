import { NextResponse } from 'next/server';
import { auth } from '@/lib/api';

export async function GET() {
  try {
    const user = await auth.getCurrentUser();
    return NextResponse.json(user);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get user data' },
      { status: 401 }
    );
  }
} 