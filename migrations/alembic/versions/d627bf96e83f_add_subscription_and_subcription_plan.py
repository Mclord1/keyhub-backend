"""add subscription and subcription plan

Revision ID: d627bf96e83f
Revises: 8cd6067b54c5
Create Date: 2023-10-09 09:40:36.314305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd627bf96e83f'
down_revision = '8cd6067b54c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subcription_plan', sa.Column('bill_cycle', sa.String(length=350), nullable=True))
    op.add_column('subcription_plan', sa.Column('description', sa.String(length=350), nullable=True))
    op.add_column('subcription_plan', sa.Column('features', sa.JSON(), nullable=True))
    op.add_column('subcription_plan', sa.Column('amount', sa.String(length=250), nullable=True))
    op.add_column('subcription_plan', sa.Column('created_by', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'subcription_plan', ['name'])
    op.create_foreign_key(None, 'subcription_plan', 'user', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'subcription_plan', type_='foreignkey')
    op.drop_constraint(None, 'subcription_plan', type_='unique')
    op.drop_column('subcription_plan', 'created_by')
    op.drop_column('subcription_plan', 'amount')
    op.drop_column('subcription_plan', 'features')
    op.drop_column('subcription_plan', 'description')
    op.drop_column('subcription_plan', 'bill_cycle')
    # ### end Alembic commands ###
