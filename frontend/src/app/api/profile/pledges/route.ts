import { NextResponse } from 'next/server';
import { pledges } from '@/lib/api';
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
    const data = await pledges.getAll();
    const userPledges = data.filter(
      (pledge) => pledge.user_id === user.id
    );
    return NextResponse.json(userPledges);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get pledges' },
      { status: 500 }
    );
  }
}

export async function POST(request: Request) {
  try {
    const { user } = useAuth();
    if (!user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }
    const body = await request.json();
    const data = await pledges.create({
      ...body,
      user_id: user.id,
    });
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create pledge' },
      { status: 500 }
    );
  }
} 