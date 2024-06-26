"""add phone_number column to User model

Revision ID: a08f16984939
Revises: 704a42091e74
Create Date: 2024-05-25 11:09:53.534584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a08f16984939'
down_revision = '704a42091e74'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_number', sa.String(length=32), nullable=False, server_default=''))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('phone_number')

    # ### end Alembic commands ###
