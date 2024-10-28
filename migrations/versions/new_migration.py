"""Update resume template reference

Revision ID: new_template_migration
Revises: 1039d54ead88
Create Date: 2024-10-28 21:45:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'new_template_migration'
down_revision = '1039d54ead88'
branch_labels = None
depends_on = None

def upgrade():
    # Drop the old template_id column and its foreign key
    with op.batch_alter_table('resumes', schema=None) as batch_op:
        batch_op.drop_constraint('fk_resume_template', type_='foreignkey')
        batch_op.drop_column('template_id')
        
        # Add the new template_name column with foreign key
        batch_op.add_column(sa.Column('template_name', sa.String(100), nullable=True))
        batch_op.create_foreign_key(
            'fk_resume_template_name',
            'templates',
            ['template_name'],
            ['name']
        )

def downgrade():
    with op.batch_alter_table('resumes', schema=None) as batch_op:
        batch_op.drop_constraint('fk_resume_template_name', type_='foreignkey')
        batch_op.drop_column('template_name')
        
        # Restore the old template_id column
        batch_op.add_column(sa.Column('template_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_resume_template',
            'templates',
            ['template_id'],
            ['id']
        )
