"""empty message

Revision ID: 834d35b7394a
Revises: 2df6f77426b8
Create Date: 2024-06-13 09:58:01.878819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '834d35b7394a'
down_revision = '2df6f77426b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=32), nullable=False),
    sa.Column('country', sa.String(length=32), nullable=False),
    sa.Column('town', sa.String(length=32), nullable=False),
    sa.Column('postal_code', sa.String(length=8), nullable=False),
    sa.Column('street', sa.String(length=32), nullable=False),
    sa.Column('street_number', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tractor_head',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(length=16), nullable=False),
    sa.Column('registration_number', sa.String(length=8), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('registration_number')
    )
    op.create_table('trailer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=16), nullable=False),
    sa.Column('registration_number', sa.String(length=7), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('registration_number')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=16), nullable=False),
    sa.Column('first_name', sa.String(length=16), nullable=False),
    sa.Column('last_name', sa.String(length=32), nullable=False),
    sa.Column('phone_number', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('transportation_order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.Date(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('planned_delivery_date', sa.Date(), nullable=False),
    sa.Column('trailer_type', sa.String(length=16), nullable=False),
    sa.Column('tractor_head', sa.Integer(), nullable=True),
    sa.Column('trailer', sa.Integer(), nullable=True),
    sa.Column('load_weight', sa.Integer(), nullable=False),
    sa.Column('loading_place', sa.Integer(), nullable=False),
    sa.Column('delivery_place', sa.Integer(), nullable=False),
    sa.Column('driver', sa.Integer(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.ForeignKeyConstraint(['delivery_place'], ['company.id'], ),
    sa.ForeignKeyConstraint(['driver'], ['user.id'], ),
    sa.ForeignKeyConstraint(['loading_place'], ['company.id'], ),
    sa.ForeignKeyConstraint(['tractor_head'], ['tractor_head.id'], ),
    sa.ForeignKeyConstraint(['trailer'], ['trailer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transportation_order')
    op.drop_table('user')
    op.drop_table('trailer')
    op.drop_table('tractor_head')
    op.drop_table('company')
    # ### end Alembic commands ###
