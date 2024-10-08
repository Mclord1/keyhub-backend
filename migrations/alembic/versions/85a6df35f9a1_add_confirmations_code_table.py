"""add confirmations code table

Revision ID: 85a6df35f9a1
Revises: f4cf4858e7a8
Create Date: 2023-08-30 18:18:59.214779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85a6df35f9a1'
down_revision = 'f4cf4858e7a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('confirmation_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('code', sa.String(length=150), nullable=True),
    sa.Column('msisdn', sa.String(length=150), nullable=True),
    sa.Column('counter', sa.Integer(), nullable=True),
    sa.Column('expiration', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('confirmation_code')
    # ### end Alembic commands ###
