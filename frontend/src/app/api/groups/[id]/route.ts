import { NextResponse } from 'next/server';
import { groups } from '@/lib/api';

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const data = await groups.getById(parseInt(params.id));
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to get group' },
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
    const data = await groups.update(parseInt(params.id), body);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to update group' },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    await groups.delete(parseInt(params.id));
    return NextResponse.json({ success: true });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to delete group' },
      { status: 500 }
    );
  }
} 