"""Update user for login

Revision ID: b37dfcf5875c
Revises: 0358443959d4
Create Date: 2017-03-08 17:03:06.062318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b37dfcf5875c'
down_revision = '0358443959d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('default', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('permissions', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('ix_roles_default'), ['default'], unique=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=64), nullable=True))
        batch_op.create_index(batch_op.f('ix_users_username'), ['username'], unique=True)
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=64), nullable=True))
        batch_op.drop_index(batch_op.f('ix_users_username'))
        batch_op.drop_column('username')

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_roles_default'))
        batch_op.drop_column('permissions')
        batch_op.drop_column('default')

    # ### end Alembic commands ###
