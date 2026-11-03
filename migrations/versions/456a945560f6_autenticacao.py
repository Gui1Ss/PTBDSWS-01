"""autenticacao: email, senha e confirmacao de conta (aula 090)

Revision ID: 456a945560f6
Revises: 38c4e85512a9
Create Date: 2026-11-03

"""
from alembic import op
import sqlalchemy as sa

revision = '456a945560f6'
down_revision = '38c4e85512a9'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('password_hash', sa.String(length=256), nullable=True))
        batch_op.add_column(sa.Column('confirmed', sa.Boolean(), nullable=True))
        batch_op.create_index('ix_users_email', ['email'], unique=True)


def downgrade():
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_index('ix_users_email')
        batch_op.drop_column('confirmed')
        batch_op.drop_column('password_hash')
        batch_op.drop_column('email')
