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
      email: data.email,
      phone: data.phone,
      full_name: data.full_name,
      role: data.role,
      is_active: data.is_active,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get settings' },
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
      email: body.email,
      phone: body.phone,
      full_name: body.full_name,
    });
    return NextResponse.json({
      email: data.email,
      phone: data.phone,
      full_name: data.full_name,
      role: data.role,
      is_active: data.is_active,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to update settings' },
      { status: 500 }
    );
  }
} 