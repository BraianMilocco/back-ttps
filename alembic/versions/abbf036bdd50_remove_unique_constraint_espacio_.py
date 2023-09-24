"""remove_unique_constraint_espacio_obligado_id

Revision ID: abbf036bdd50
Revises: dad538f936fc
Create Date: 2023-09-23 21:14:45.451186

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "abbf036bdd50"
down_revision: Union[str, None] = "dad538f936fc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Crear una nueva tabla temporal sin las restricciones UNIQUE
    op.create_table(
        "visitas_temp",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("fecha", sa.DateTime),
        sa.Column("observaciones", sa.String),
        sa.Column("resultado", sa.String, nullable=False),
        sa.Column(
            "espacio_obligado_id", sa.Integer, sa.ForeignKey("espacios_obligados.id")
        ),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.CheckConstraint("resultado IN ('Aprobado', 'Rechazado', 'Dado de baja')"),
    )

    # Copiar los datos de la tabla original a la tabla temporal
    op.execute("INSERT INTO visitas_temp SELECT * FROM visitas")

    # Eliminar la tabla original
    op.drop_table("visitas")

    # Renombrar la tabla temporal al nombre original
    op.rename_table("visitas_temp", "visitas")


def downgrade() -> None:
    # En este caso, la operación downgrade es más complicada ya que SQLite no soporta añadir restricciones UNIQUE directamente
    # Una opción sería crear otra tabla temporal, copiar los datos, y hacer las validaciones necesarias para asegurar que
    # los datos cumplen con las restricciones UNIQUE antes de renombrar la tabla.
    # Dada la complejidad, se podría considerar no soportar el downgrade o lanzar una excepción indicando que no es soportado.
    raise NotImplementedError("Downgrade not supported")
