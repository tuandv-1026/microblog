"""add_user_id_to_comments

Revision ID: 34a11d4c7ed0
Revises: 
Create Date: 2026-02-05 04:27:36.739546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34a11d4c7ed0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add user_id column to comments table
    op.add_column('comments', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_comments_user_id', 'comments', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_index('ix_comments_user_id', 'comments', ['user_id'])


def downgrade() -> None:
    # Remove user_id column from comments table
    op.drop_index('ix_comments_user_id', 'comments')
    op.drop_constraint('fk_comments_user_id', 'comments', type_='foreignkey')
    op.drop_column('comments', 'user_id')
