"""agregar notificacion

Revision ID: c7b2ee075120
Revises: b0a62e2d07dd
Create Date: 2023-09-24 13:45:09.032134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7b2ee075120'
down_revision: Union[str, None] = 'b0a62e2d07dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
