"""add countries and states

Revision ID: 68eb68bdc226
Revises: b4dc42e6387a
Create Date: 2023-10-07 18:20:31.028728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68eb68bdc226'
down_revision = 'b4dc42e6387a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_code', sa.String(length=250), nullable=True),
    sa.Column('country_name', sa.String(length=250), nullable=True),
    sa.Column('country_currency', sa.String(length=250), nullable=True),
    sa.Column('country_capital', sa.String(length=250), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('state',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('state_name', sa.String(length=250), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_constraint('teacher_school_id_fkey', 'teacher', type_='foreignkey')
    op.drop_column('teacher', 'school_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teacher', sa.Column('school_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('teacher_school_id_fkey', 'teacher', 'school', ['school_id'], ['id'])
    op.drop_table('state')
    op.drop_table('country')
    # ### end Alembic commands ###
