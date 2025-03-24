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
    return NextResponse.json({
      theme: data.theme,
      language: data.language,
      timezone: data.timezone,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get preferences' },
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
    const data = await users.update(user.id, {
      theme: body.theme,
      language: body.language,
      timezone: body.timezone,
    });
    return NextResponse.json({
      theme: data.theme,
      language: data.language,
      timezone: data.timezone,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to update preferences' },
      { status: 500 }
    );
  }
} 