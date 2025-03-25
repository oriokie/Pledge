"""add status to projects

Revision ID: add_status_to_projects
Revises: 4918557ea2b5
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_status_to_projects'
down_revision = '4918557ea2b5'
branch_labels = None
depends_on = None

def upgrade():
    # Add status column to projects table
    op.add_column('projects', sa.Column('status', sa.String(), nullable=True, server_default='active'))

def downgrade():
    # Remove status column from projects table
    op.drop_column('projects', 'status') 