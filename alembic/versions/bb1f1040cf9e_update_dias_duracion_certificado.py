"""update_dias_duracion_certificado

Revision ID: bb1f1040cf9e
Revises: 460d8aaeefa4
Create Date: 2023-09-23 20:35:29.414761

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bb1f1040cf9e"
down_revision: Union[str, None] = "460d8aaeefa4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = "provincias"


def upgrade() -> None:
    op.execute(
        sa.text(
            f"""
            UPDATE {table_name}
            SET dias_duracion_certificado = 2
            WHERE id BETWEEN 1 AND 23
            """
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            f"""
            UPDATE {table_name}
            SET dias_duracion_certificado = NULL
            WHERE id BETWEEN 1 AND 23
            """
        )
    )
