"""added uid to user table

Revision ID: 536e53cdcb7a
Revises: 
Create Date: 2021-04-19 01:28:21.928757

"""
from alembic import op
import sqlalchemy as sa
import secrets


# revision identifiers, used by Alembic.
revision = '536e53cdcb7a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column("uid", sa.String(200), default = secrets.token_urlsafe))


def downgrade():
    pass
