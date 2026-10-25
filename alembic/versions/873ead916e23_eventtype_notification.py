"""eventtype notification

Revision ID: 873ead916e23
Revises: e08eee9ee177
Create Date: 2026-10-25 20:43:12.873592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '873ead916e23'
down_revision: Union[str, Sequence[str], None] = 'e08eee9ee177'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE eventtype ADD VALUE 'NOTIFICATION'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
