"""feat : add learning_group_subscription table

Revision ID: 4ebfaae11480
Revises: 4e51560216e6
Create Date: 2023-11-22 07:11:06.455208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ebfaae11480'
down_revision = '4e51560216e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('learning_group_subscription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('learning_group_id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['learning_group_id'], ['learning_group.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['parent_id'], ['parent.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('learning_group_subscription')
    # ### end Alembic commands ###
