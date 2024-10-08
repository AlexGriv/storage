"""by field

Revision ID: 8d8ec66046cf
Revises: a2dae17817c6
Create Date: 2023-10-09 22:05:45.476973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d8ec66046cf'
down_revision = 'a2dae17817c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role', sa.String(length=20), nullable=True))
    op.create_index(op.f('ix_user_role'), 'user', ['role'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_role'), table_name='user')
    op.drop_column('user', 'role')
    # ### end Alembic commands ###
