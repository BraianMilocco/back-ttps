"""remove_unique_constraint_espacio_obligado_id en dea

Revision ID: b0a62e2d07dd
Revises: abbf036bdd50
Create Date: 2023-09-24 13:14:59.420248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b0a62e2d07dd"
down_revision: Union[str, None] = "abbf036bdd50"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Define la nueva tabla temporal
    op.create_table(
        "temp_deas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("numero_serie", sa.String(), nullable=False, unique=True),
        sa.Column("nombre", sa.String(), nullable=True),
        sa.Column("marca", sa.String(), nullable=True),
        sa.Column("modelo", sa.String(), nullable=True),
        sa.Column("solidario", sa.Boolean(), nullable=True, default=False),
        sa.Column("activo", sa.Boolean(), nullable=True, default=False),
        sa.Column("fecha_ultimo_mantenimiento", sa.DateTime(), nullable=True),
        sa.Column("espacio_obligado_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["espacio_obligado_id"], ["espacios_obligados.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Copia todos los datos de la tabla 'deas' a la tabla temporal 'temp_deas'
    op.execute("INSERT INTO temp_deas SELECT * FROM deas")

    # Elimina la tabla original 'deas'
    op.drop_table("deas")

    # Renombra la tabla temporal 'temp_deas' a 'deas'
    op.rename_table("temp_deas", "deas")


def downgrade():
    # Define la estructura original de la tabla 'deas' con el constraint 'unique'
    op.create_table(
        "temp_deas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("numero_serie", sa.String(), nullable=False, unique=True),
        sa.Column("nombre", sa.String(), nullable=True),
        sa.Column("marca", sa.String(), nullable=True),
        sa.Column("modelo", sa.String(), nullable=True),
        sa.Column("solidario", sa.Boolean(), nullable=True, default=False),
        sa.Column("activo", sa.Boolean(), nullable=True, default=False),
        sa.Column("fecha_ultimo_mantenimiento", sa.DateTime(), nullable=True),
        sa.Column("espacio_obligado_id", sa.Integer(), nullable=False, unique=True),
        sa.ForeignKeyConstraint(["espacio_obligado_id"], ["espacios_obligados.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Copia todos los datos de la tabla 'deas' a la tabla temporal 'temp_deas'
    op.execute("INSERT INTO temp_deas SELECT * FROM deas")

    # Elimina la tabla original 'deas'
    op.drop_table("deas")

    # Renombra la tabla temporal 'temp_deas' a 'deas'
    op.rename_table("temp_deas", "deas")
