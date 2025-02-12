"""Add is_active field to Template model

Revision ID: d7fdb0ab6fb7
Revises: 11c44f17304e
Create Date: 2024-10-28 09:56:48.383406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7fdb0ab6fb7'
down_revision = '11c44f17304e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('template', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('template', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###
