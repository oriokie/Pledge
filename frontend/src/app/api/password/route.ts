import { NextResponse } from 'next/server';
import { users } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';

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
    const { currentPassword, newPassword } = body;

    // Update password using the update method
    await users.update(user.id, {
      password: newPassword,
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to update password' },
      { status: 500 }
    );
  }
} 