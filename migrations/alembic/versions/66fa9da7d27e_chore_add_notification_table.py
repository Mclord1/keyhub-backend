"""chore : add notification table

Revision ID: 66fa9da7d27e
Revises: 63e0a258a676
Create Date: 2023-11-25 17:46:38.035794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66fa9da7d27e'
down_revision = '63e0a258a676'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=255), nullable=False),
    sa.Column('data', sa.JSON(), nullable=True),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint('_user_learning_group_uc', 'learning_group_subscription', ['learning_group_id', 'user_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_user_learning_group_uc', 'learning_group_subscription', type_='unique')
    op.drop_table('notification')
    # ### end Alembic commands ###
