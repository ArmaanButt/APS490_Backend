"""Create targets table

Revision ID: b28bc0e40bb2
Revises: 4e3a3bbab80c
Create Date: 2017-01-12 08:11:42.910123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b28bc0e40bb2'
down_revision = '4e3a3bbab80c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'targets',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('is_working', sa.Boolean, nullable=False),
        sa.Column('size', sa.Float, nullable=False),
        sa.Column('is_enabled', sa.Boolean, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4',
    )


def downgrade():
    op.drop_table('targets')
