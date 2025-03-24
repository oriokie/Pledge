import { NextResponse } from 'next/server';
import { contributions } from '@/lib/api';
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
    const data = await contributions.getAll();
    const userContributions = data.filter(
      (contribution) => contribution.user_id === user.id
    );
    return NextResponse.json(userContributions);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get contributions' },
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
    const data = await contributions.create({
      ...body,
      user_id: user.id,
    });
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to create contribution' },
      { status: 500 }
    );
  }
} 