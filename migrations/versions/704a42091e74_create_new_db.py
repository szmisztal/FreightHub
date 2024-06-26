"""create new db

Revision ID: 704a42091e74
Revises: 
Create Date: 2024-05-22 10:39:06.404093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '704a42091e74'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.String(length=32), nullable=False),
    sa.Column('country', sa.String(length=32), nullable=False),
    sa.Column('town', sa.String(length=32), nullable=False),
    sa.Column('postal_code', sa.String(length=16), nullable=False),
    sa.Column('street', sa.String(length=32), nullable=False),
    sa.Column('street_number', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=16), nullable=False),
    sa.Column('first_name', sa.String(length=16), nullable=False),
    sa.Column('last_name', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=16), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('transportation_order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('planned_delivery_date', sa.Date(), nullable=False),
    sa.Column('trailer_type', sa.String(length=16), nullable=False),
    sa.Column('load_weight', sa.Integer(), nullable=False),
    sa.Column('loading_place', sa.Integer(), nullable=False),
    sa.Column('delivery_place', sa.Integer(), nullable=False),
    sa.Column('driver', sa.Integer(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], name='fk_transportation_order_creation_by'),
    sa.ForeignKeyConstraint(['delivery_place'], ['company.id'], name='fk_transportation_order_delivery_place'),
    sa.ForeignKeyConstraint(['driver'], ['user.id'], name='fk_transportation_order_driver'),
    sa.ForeignKeyConstraint(['loading_place'], ['company.id'], name='fk_transportation_order_loading_place'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transportation_order')
    op.drop_table('user')
    op.drop_table('company')
    # ### end Alembic commands ###
