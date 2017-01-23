"""Create sessions table

Revision ID: c5dbc4b3df2a
Revises: b28bc0e40bb2
Create Date: 2017-01-12 09:44:03.052868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5dbc4b3df2a'
down_revision = 'b28bc0e40bb2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('target_id', sa.Integer, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['target_id'],
            ['targets.id'],
            ondelete='CASCADE',
        ),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4',
    )


def downgrade():
    op.drop_table('sessions')
