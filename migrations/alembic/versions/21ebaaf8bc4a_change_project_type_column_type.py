"""Change project_type column type

Revision ID: 21ebaaf8bc4a
Revises: be40fcc56a71
Create Date: 2023-11-03 07:31:19.281701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21ebaaf8bc4a'
down_revision = 'be40fcc56a71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('project', 'project_type', type_=sa.String(length=350))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('project', 'project_type', type_=sa.JSON())
    # ### end Alembic commands ###
