"""Add created_by_id to projects

Revision ID: add_created_by_to_projects
Revises: update_project_columns
Create Date: 2024-03-25 19:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_created_by_to_projects'
down_revision = 'update_project_columns'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Add created_by_id column to projects table
    op.add_column('projects', sa.Column('created_by_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_projects_created_by_id',
        'projects', 'users',
        ['created_by_id'], ['id'],
        ondelete='SET NULL'
    )

def downgrade() -> None:
    # Remove the foreign key constraint first
    op.drop_constraint('fk_projects_created_by_id', 'projects', type_='foreignkey')
    # Then remove the column
    op.drop_column('projects', 'created_by_id') 