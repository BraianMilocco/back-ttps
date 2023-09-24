"""quitar unique al user en visitas

Revision ID: f5ab8bcf6fe2
Revises: 86791c7ac189
Create Date: 2023-09-23 21:02:25.410678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5ab8bcf6fe2'
down_revision: Union[str, None] = '86791c7ac189'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
