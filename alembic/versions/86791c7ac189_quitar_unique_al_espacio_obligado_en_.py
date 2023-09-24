"""quitar unique al espacio obligado en visitas

Revision ID: 86791c7ac189
Revises: bb1f1040cf9e
Create Date: 2023-09-23 21:01:53.585033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86791c7ac189'
down_revision: Union[str, None] = 'bb1f1040cf9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
