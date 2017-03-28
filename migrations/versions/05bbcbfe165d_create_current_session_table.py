"""Create current session table

Revision ID: 05bbcbfe165d
Revises: cf6135d09a0d
Create Date: 2017-03-28 16:44:59.051261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05bbcbfe165d'
down_revision = 'cf6135d09a0d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'current_session',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('current_session_id', sa.Integer, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4',
    )


def downgrade():
    op.drop_table('current_session')
