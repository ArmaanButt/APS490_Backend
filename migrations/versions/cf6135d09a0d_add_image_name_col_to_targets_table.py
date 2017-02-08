"""add image_name col to targets table

Revision ID: cf6135d09a0d
Revises: df6076862356
Create Date: 2017-02-08 11:52:57.636937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf6135d09a0d'
down_revision = 'df6076862356'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'targets',
        sa.Column('image_name', sa.VARCHAR(128)),
    )


def downgrade():
    op.drop_column('targets', 'image_name')
