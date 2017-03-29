"""add user_id, target_id to current_session table

Revision ID: 81d19349d95f
Revises: 5b8537b38070
Create Date: 2017-03-28 18:48:59.080229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81d19349d95f'
down_revision = '5b8537b38070'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('current_session')
    op.create_table(
        'current_session',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('session_id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('target_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(
            ['session_id'],
            ['sessions.id'],
            ondelete='CASCADE',
        ),
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
    op.drop_table('current_session')
    op.create_table(
        'current_session',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('current_session_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(
            ['current_session_id'],
            ['sessions.id'],
            ondelete='CASCADE',
        ),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4',
    )
