"""quitar unique al user en visitas

Revision ID: dad538f936fc
Revises: f5ab8bcf6fe2
Create Date: 2023-09-23 21:03:56.887165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dad538f936fc'
down_revision: Union[str, None] = 'f5ab8bcf6fe2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
