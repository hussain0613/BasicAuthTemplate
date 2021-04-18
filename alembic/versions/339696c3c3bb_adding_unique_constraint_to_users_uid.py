"""adding unique constraint to users.uid

Revision ID: 339696c3c3bb
Revises: 536e53cdcb7a
Create Date: 2021-04-19 02:58:36.798450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '339696c3c3bb'
down_revision = '536e53cdcb7a'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.create_unique_constraint('uq_user_uid', ['uid'])


def downgrade():
    pass
