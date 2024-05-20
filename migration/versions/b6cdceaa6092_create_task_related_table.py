"""Create Task Related Table

Revision ID: b6cdceaa6092
Revises: 
Create Date: 2024-05-19 13:04:45.414403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6cdceaa6092'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

task_status_enum = sa.Enum('DRAFT', 'OPEN', 'IN_PROGRESS', 'DONE', 'CANCELLED', 'DELETED', name="taskstatus")
task_perm_type_enum = sa.Enum('USER', 'TEAM', name='taskpermissiontype')
task_perm_level_enum = sa.Enum('VIEW', 'EDIT', 'DELETE', name='taskpermissionlevel')


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('permission_entity_id', sa.VARCHAR(38), nullable=False),
        sa.Column('username', sa.VARCHAR(32), nullable=False),
        sa.Column('firstname', sa.VARCHAR(255), nullable=False),
        sa.Column('lastname', sa.VARCHAR(255), nullable=False),
        sa.Column('email', sa.VARCHAR(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True)
    )
    
    op.create_table(
        'task',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('version', sa.Integer, nullable=False),
        sa.Column('topic', sa.VARCHAR, nullable=False),
        sa.Column('description', sa.TEXT, nullable=True),
        sa.Column('status', task_status_enum, nullable=False),
        sa.Column('created_by', sa.UUID, sa.ForeignKey('user.id'), nullable=False),
        sa.Column('assignee', sa.UUID, sa.ForeignKey('user.id'), nullable=True),
        sa.Column('use_permission', sa.Boolean, default=False, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True)
    )
    
    op.create_table(
        'task_history',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('task_id', sa.UUID, sa.ForeignKey('task.id'), nullable=False),
        sa.Column('version', sa.Integer, nullable=False),
        sa.Column('topic', sa.VARCHAR, nullable=False),
        sa.Column('description', sa.TEXT, nullable=True),
        sa.Column('status', task_status_enum, nullable=False),
        sa.Column('assignee', sa.UUID, sa.ForeignKey('user.id'), nullable=True),
        sa.Column('use_permission', sa.Boolean, default=False, nullable=False),
        sa.Column('edited_by', sa.UUID, sa.ForeignKey('user.id'), nullable=False),
        sa.Column('edited_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True)
    )
    
    op.create_table(
        'team',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('permission_entity_id', sa.VARCHAR(38), nullable=False),
        sa.Column('name', sa.VARCHAR(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_updated_at', sa.DateTime(), nullable=False),
        sa.Column('deleted_at', sa.DateTime(), nullable=True)
    )
    
    op.create_table(
        'team_member',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('team_id', sa.UUID, sa.ForeignKey('team.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.UUID, sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    )
    
    op.create_table(
        'task_permision',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('task_id', sa.UUID, sa.ForeignKey('task.id'), nullable=False),
        sa.Column('permission_entity_id', sa.VARCHAR(38), nullable=False),
        sa.Column('permission_type', task_perm_type_enum, nullable=False),
        sa.Column('permissionLevel', task_perm_level_enum, nullable=False)
    )

def downgrade() -> None:
    op.drop_table('task_permision')
    op.drop_table('team_member')
    op.drop_table('team')
    op.drop_table('task_history')
    op.drop_table('task')
    op.drop_table('user')
    task_status_enum.drop(op.get_bind())
    task_perm_type_enum.drop(op.get_bind())
    task_perm_level_enum.drop(op.get_bind())
