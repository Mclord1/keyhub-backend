"""chore : update school role, learning-group, project models

Revision ID: d7b5cf8b5402
Revises: 751a19ecca00
Create Date: 2023-10-23 21:50:24.402871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7b5cf8b5402'
down_revision = '751a19ecca00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teacher_student')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('teacher_student',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('student_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('last_updated', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name='teacher_student_student_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['teacher_id'], ['teacher.id'], name='teacher_student_teacher_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='teacher_student_pkey')
    )
    # ### end Alembic commands ###
