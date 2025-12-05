"""empty message

Revision ID: d6f91f7cbb3b
Revises: 33a8982d3940, 7217bdb87322
Create Date: 2025-12-05 22:22:14.015188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6f91f7cbb3b'
down_revision: Union[str, Sequence[str], None] = ('33a8982d3940', '7217bdb87322')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
