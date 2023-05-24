"""empty message

Revision ID: 2c26762d070b
Revises: 
Create Date: 2023-05-22 10:48:25.130675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c26762d070b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('boss_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['boss_id'], ['Employee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.CHAR(length=20), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('status', sa.Enum('open', 'active', 'resolved', name='task_status'), nullable=False),
    sa.Column('creation', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('EmployeeTask',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee', sa.Integer(), nullable=False),
    sa.Column('task', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['employee'], ['Employee.id'], ),
    sa.ForeignKeyConstraint(['task'], ['Task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee', sa.Integer(), nullable=True),
    sa.Column('task', sa.Integer(), nullable=False),
    sa.Column('creation', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['employee'], ['Employee.id'], ),
    sa.ForeignKeyConstraint(['task'], ['Task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee', sa.Integer(), nullable=False),
    sa.Column('start', sa.DateTime(), nullable=False),
    sa.Column('end', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['employee'], ['Employee.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event', sa.Integer(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['event'], ['Event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('EmployeeChange',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event', sa.Integer(), nullable=False),
    sa.Column('employee', sa.Integer(), nullable=False),
    sa.Column('action', sa.Enum('add', 'remove', name='employee_change_type'), nullable=False),
    sa.ForeignKeyConstraint(['employee'], ['Employee.id'], ),
    sa.ForeignKeyConstraint(['event'], ['Event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ReportPart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('report', sa.Integer(), nullable=False),
    sa.Column('origin_report', sa.Integer(), nullable=True),
    sa.Column('origin_task', sa.Integer(), nullable=True),
    sa.Column('origin_type', sa.Enum('report', 'task', name='origin_report_part_type'), nullable=False),
    sa.Column('comment', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['origin_report'], ['Report.id'], ),
    sa.ForeignKeyConstraint(['origin_task'], ['Task.id'], ),
    sa.ForeignKeyConstraint(['report'], ['Report.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('StatusChange',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event', sa.Integer(), nullable=False),
    sa.Column('old', sa.Enum('open', 'active', 'resolved', name='task_status'), nullable=False),
    sa.Column('new', sa.Enum('open', 'active', 'resolved', name='task_status'), nullable=False),
    sa.ForeignKeyConstraint(['event'], ['Event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('StatusChange')
    op.drop_table('ReportPart')
    op.drop_table('EmployeeChange')
    op.drop_table('Comment')
    op.drop_table('Report')
    op.drop_table('Event')
    op.drop_table('EmployeeTask')
    op.drop_table('Task')
    op.drop_table('Employee')
    # ### end Alembic commands ###
