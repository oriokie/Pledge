"""add missing contribution columns

Revision ID: 30cf7e878aef
Revises: 20240320000000
Create Date: 2025-03-24 14:02:52.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '30cf7e878aef'
down_revision = '20240320000000'
branch_labels = None
depends_on = None

def upgrade():
    # Create payment method enum
    op.execute("CREATE TYPE paymentmethod AS ENUM ('CASH', 'MOBILE_MONEY', 'BANK_TRANSFER')")
    
    # Add missing columns to contributions table
    op.add_column('contributions', sa.Column('pledge_date', sa.Date(), nullable=True))
    op.add_column('contributions', sa.Column('payment_method', postgresql.ENUM('CASH', 'MOBILE_MONEY', 'BANK_TRANSFER', name='paymentmethod'), nullable=True))
    op.add_column('contributions', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('contributions', sa.Column('status', sa.String(), default='pending', nullable=True))
    op.add_column('contributions', sa.Column('error_message', sa.Text(), nullable=True))

def downgrade():
    # Remove added columns from contributions table
    op.drop_column('contributions', 'error_message')
    op.drop_column('contributions', 'status')
    op.drop_column('contributions', 'description')
    op.drop_column('contributions', 'payment_method')
    op.drop_column('contributions', 'pledge_date')
    
    # Drop the enum type
    op.execute('DROP TYPE paymentmethod') 