"""little changes in len() fields in models

Revision ID: 02a06dc2834a
Revises: b51c4cbe6ebf
Create Date: 2024-05-31 12:51:56.457317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02a06dc2834a'
down_revision = 'b51c4cbe6ebf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.alter_column('postal_code',
               existing_type=sa.VARCHAR(length=16),
               type_=sa.String(length=8),
               existing_nullable=False)

    with op.batch_alter_table('tractor_head', schema=None) as batch_op:
        batch_op.alter_column('registration_number',
               existing_type=sa.VARCHAR(length=16),
               type_=sa.String(length=8),
               existing_nullable=False)

    with op.batch_alter_table('trailer', schema=None) as batch_op:
        batch_op.alter_column('registration_number',
               existing_type=sa.VARCHAR(length=16),
               type_=sa.String(length=7),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trailer', schema=None) as batch_op:
        batch_op.alter_column('registration_number',
               existing_type=sa.String(length=7),
               type_=sa.VARCHAR(length=16),
               existing_nullable=False)

    with op.batch_alter_table('tractor_head', schema=None) as batch_op:
        batch_op.alter_column('registration_number',
               existing_type=sa.String(length=8),
               type_=sa.VARCHAR(length=16),
               existing_nullable=False)

    with op.batch_alter_table('company', schema=None) as batch_op:
        batch_op.alter_column('postal_code',
               existing_type=sa.String(length=8),
               type_=sa.VARCHAR(length=16),
               existing_nullable=False)

    # ### end Alembic commands ###