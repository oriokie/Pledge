import { NextResponse } from 'next/server';
import { users } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';

export async function GET() {
  try {
    const { user } = useAuth();
    if (!user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }
    const data = await users.getById(user.id);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get profile' },
      { status: 500 }
    );
  }
}

export async function PUT(request: Request) {
  try {
    const { user } = useAuth();
    if (!user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }
    const body = await request.json();
    const data = await users.update(user.id, body);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to update profile' },
      { status: 500 }
    );
  }
} 