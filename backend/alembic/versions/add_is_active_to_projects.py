"""add is_active to projects

Revision ID: add_is_active_to_projects
Revises: add_status_to_projects
Create Date: 2024-03-25 18:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_is_active_to_projects'
down_revision = 'add_status_to_projects'
branch_labels = None
depends_on = None

def upgrade():
    # Add is_active column to projects table
    op.add_column('projects', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'))

def downgrade():
    # Remove is_active column from projects table
    op.drop_column('projects', 'is_active') 