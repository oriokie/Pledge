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
      email_notifications: data.email_notifications,
      sms_notifications: data.sms_notifications,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get notifications' },
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
      email_notifications: body.email_notifications,
      sms_notifications: body.sms_notifications,
    });
    return NextResponse.json({
      email_notifications: data.email_notifications,
      sms_notifications: data.sms_notifications,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to update notifications' },
      { status: 500 }
    );
  }
} 