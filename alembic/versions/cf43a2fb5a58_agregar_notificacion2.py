"""agregar notificacion2

Revision ID: cf43a2fb5a58
Revises: c7b2ee075120
Create Date: 2023-09-24 13:46:59.605451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cf43a2fb5a58"
down_revision: Union[str, None] = "c7b2ee075120"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Crear la tabla notificaciones
    op.create_table(
        "notificaciones",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("texto", sa.String, index=True, nullable=False),
        sa.Column("fecha", sa.DateTime, default=sa.text("current_timestamp")),
        sa.Column(
            "espacio_obligado_id",
            sa.Integer,
            sa.ForeignKey("espacios_obligados.id"),
            nullable=False,
        ),
    )


def downgrade():
    # Eliminar la tabla notificaciones
    op.drop_table("notificaciones")
