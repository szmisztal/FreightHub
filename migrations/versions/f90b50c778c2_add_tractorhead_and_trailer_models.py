from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f90b50c778c2'
down_revision = 'a08f16984939'
branch_labels = None
depends_on = None


def upgrade():
    # Check if table tractor_head exists before creating
    if not op.get_bind().dialect.has_table(op.get_bind(), 'tractor_head'):
        op.create_table('tractor_head',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('brand', sa.String(length=16), nullable=False),
            sa.Column('registration_number', sa.String(length=16), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )

    # Check if table trailer exists before creating
    if not op.get_bind().dialect.has_table(op.get_bind(), 'trailer'):
        op.create_table('trailer',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('type', sa.String(length=16), nullable=False),
            sa.Column('registration_number', sa.String(length=16), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )

    with op.batch_alter_table('transportation_order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tractor_head', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('trailer', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_transportation_order_trailer', 'trailer', ['trailer'], ['id'])
        batch_op.create_foreign_key('fk_transportation_order_tractor_head', 'tractor_head', ['tractor_head'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('transportation_order', schema=None) as batch_op:
        batch_op.drop_constraint('fk_transportation_order_trailer', type_='foreignkey')
        batch_op.drop_constraint('fk_transportation_order_tractor_head', type_='foreignkey')
        batch_op.drop_column('trailer')
        batch_op.drop_column('tractor_head')

    op.drop_table('trailer')
    op.drop_table('tractor_head')
    # ### end Alembic commands ###
