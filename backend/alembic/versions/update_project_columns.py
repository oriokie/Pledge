"""update project columns

Revision ID: update_project_columns
Revises: add_is_active_to_projects
Create Date: 2024-03-25 19:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'update_project_columns'
down_revision = 'add_is_active_to_projects'
branch_labels = None
depends_on = None

def upgrade():
    # Update column types and constraints
    op.alter_column('projects', 'description',
        existing_type=sa.Text(),
        nullable=True)
    op.alter_column('projects', 'start_date',
        existing_type=sa.Date(),
        nullable=True)
    op.alter_column('projects', 'end_date',
        existing_type=sa.Date(),
        nullable=True)
    op.alter_column('projects', 'status',
        existing_type=sa.String(),
        server_default='active',
        nullable=False)
    op.alter_column('projects', 'created_at',
        existing_type=sa.Date(),
        type_=sa.DateTime(timezone=True),
        server_default=sa.text('now()'),
        nullable=False)
    op.alter_column('projects', 'updated_at',
        existing_type=sa.Date(),
        type_=sa.DateTime(timezone=True),
        server_default=sa.text('now()'),
        nullable=False)

def downgrade():
    # Revert column types and constraints
    op.alter_column('projects', 'description',
        existing_type=sa.Text(),
        nullable=False)
    op.alter_column('projects', 'start_date',
        existing_type=sa.Date(),
        nullable=False)
    op.alter_column('projects', 'end_date',
        existing_type=sa.Date(),
        nullable=False)
    op.alter_column('projects', 'status',
        existing_type=sa.String(),
        server_default=None,
        nullable=True)
    op.alter_column('projects', 'created_at',
        existing_type=sa.DateTime(timezone=True),
        type_=sa.Date(),
        server_default=None,
        nullable=True)
    op.alter_column('projects', 'updated_at',
        existing_type=sa.DateTime(timezone=True),
        type_=sa.Date(),
        server_default=None,
        nullable=True) 