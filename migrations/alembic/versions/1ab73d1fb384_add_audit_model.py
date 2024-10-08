"""Add audit model

Revision ID: 1ab73d1fb384
Revises: e6f47cec29c7
Create Date: 2023-10-29 16:06:25.840749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ab73d1fb384'
down_revision = 'e6f47cec29c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subcription_features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=350), nullable=True),
    sa.Column('description', sa.String(length=350), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column('audit', sa.Column('action', sa.String(length=350), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('audit', 'action')
    op.drop_table('subcription_features')
    # ### end Alembic commands ###
