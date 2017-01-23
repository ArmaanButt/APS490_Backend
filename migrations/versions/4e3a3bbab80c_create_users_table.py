"""Create users table

Revision ID: 4e3a3bbab80c
Revises: 
Create Date: 2017-01-08 00:15:19.201005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e3a3bbab80c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.INTEGER, primary_key=True, nullable=False),
        sa.Column('username', sa.VARCHAR(128), nullable=False, unique=True),
        sa.Column('password', sa.VARCHAR(1024), nullable=False),
        sa.Column('role', sa.VARCHAR(128), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4',
    )


def downgrade():
    op.drop_table('users')
