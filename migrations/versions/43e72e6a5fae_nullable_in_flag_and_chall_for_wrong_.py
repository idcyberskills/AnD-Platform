"""Nullable in flag and chall for wrong submission

Revision ID: 43e72e6a5fae
Revises: 1f72fddcddc8
Create Date: 2024-07-24 12:45:57.220286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43e72e6a5fae'
down_revision = '1f72fddcddc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('submission', schema=None) as batch_op:
        batch_op.alter_column('challenge_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('flag_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('submission', schema=None) as batch_op:
        batch_op.alter_column('flag_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('challenge_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
