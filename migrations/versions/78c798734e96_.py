"""empty message

Revision ID: 78c798734e96
Revises: a5ae8f094c88
Create Date: 2024-05-13 11:57:07.815374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78c798734e96'
down_revision = 'a5ae8f094c88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=16),
               existing_nullable=False)
        batch_op.alter_column('first_name',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=16),
               existing_nullable=False)
        batch_op.alter_column('last_name',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=16),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=128),
               existing_nullable=False)
        batch_op.alter_column('role',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=16),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('role',
               existing_type=sa.String(length=16),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)
        batch_op.alter_column('last_name',
               existing_type=sa.String(length=16),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
        batch_op.alter_column('first_name',
               existing_type=sa.String(length=16),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=16),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###
