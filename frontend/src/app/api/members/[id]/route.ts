import { NextResponse } from 'next/server';
import { members } from '@/lib/api';

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const data = await members.getById(parseInt(params.id));
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get member' },
      { status: 500 }
    );
  }
}

export async function PUT(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json();
    const data = await members.update(parseInt(params.id), body);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to update member' },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    await members.delete(parseInt(params.id));
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to delete member' },
      { status: 500 }
    );
  }
} 