"""add foreing key constraint to current_session

Revision ID: 5b8537b38070
Revises: 05bbcbfe165d
Create Date: 2017-03-28 18:35:55.043225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b8537b38070'
down_revision = '05bbcbfe165d'
branch_labels = None
depends_on = None


def upgrade():
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


def downgrade():
    op.drop_table('current_session')
    op.create_table(
        'current_session',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('current_session_id', sa.Integer, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4',
    )
