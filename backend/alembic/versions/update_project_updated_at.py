"""Update project updated_at column

Revision ID: update_project_updated_at
Revises: add_created_by_to_projects
Create Date: 2024-03-25 20:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = 'update_project_updated_at'
down_revision = 'add_created_by_to_projects'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Update updated_at column to have server_default
    op.alter_column('projects', 'updated_at',
                    existing_type=sa.DateTime(timezone=True),
                    server_default=sa.text('now()'),
                    existing_nullable=False)

def downgrade() -> None:
    # Remove server_default from updated_at column
    op.alter_column('projects', 'updated_at',
                    existing_type=sa.DateTime(timezone=True),
                    server_default=None,
                    existing_nullable=False) 