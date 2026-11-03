"""initial migration

Revision ID: 38c4e85512a9
Revises:
Create Date: 2026-11-03

"""
from alembic import op
import sqlalchemy as sa

revision = '38c4e85512a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=True)


def downgrade():
    op.drop_index('ix_users_username', 'users')
    op.drop_table('users')
    op.drop_table('roles')
