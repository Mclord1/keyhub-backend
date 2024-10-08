"""add new column to parent

Revision ID: 9ae578ff16b8
Revises: 8a752ad3f1e6
Create Date: 2024-02-18 17:01:54.356464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ae578ff16b8'
down_revision = '8a752ad3f1e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('parent', sa.Column('how_you_knew_about_us', sa.Text(), nullable=True))
    op.add_column('parent', sa.Column('why_use_us', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('parent', 'why_use_us')
    op.drop_column('parent', 'how_you_knew_about_us')
    # ### end Alembic commands ###
