"""chore : add culiculum

Revision ID: ba72be53e009
Revises: ce2eb4f94811
Create Date: 2023-11-10 10:21:07.170874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba72be53e009'
down_revision = 'ce2eb4f94811'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('curriculum', sa.String(length=450), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'curriculum')
    # ### end Alembic commands ###
