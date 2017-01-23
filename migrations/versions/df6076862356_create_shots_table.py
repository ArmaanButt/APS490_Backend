"""Create shots table

Revision ID: df6076862356
Revises: c5dbc4b3df2a
Create Date: 2017-01-16 17:19:51.946730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df6076862356'
down_revision = 'c5dbc4b3df2a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'shots',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('target_id', sa.Integer, nullable=False),
        sa.Column('session_id', sa.Integer, nullable=False),
        sa.Column('coordinate_x', sa.Float, nullable=False),
        sa.Column('coordinate_y', sa.Float, nullable=False),
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
        sa.ForeignKeyConstraint(
            ['session_id'],
            ['sessions.id'],
            ondelete='CASCADE',
        ),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4',
    )


def downgrade():
    op.drop_table('shots')
