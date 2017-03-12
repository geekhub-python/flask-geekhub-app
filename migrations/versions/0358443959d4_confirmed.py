"""empty message

Revision ID: 0358443959d4
Revises: 053b5a61978d
Create Date: 2017-03-02 19:13:55.097805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0358443959d4'
down_revision = '053b5a61978d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('confirmed', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('confirmed')

    # ### end Alembic commands ###