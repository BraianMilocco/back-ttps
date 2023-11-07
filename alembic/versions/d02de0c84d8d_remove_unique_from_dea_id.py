"""remove unique from dea_id

Revision ID: d02de0c84d8d
Revises: 0e9cc95d6ffe
Create Date: 2023-11-07 17:24:19.163555

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d02de0c84d8d"
down_revision: Union[str, None] = "0e9cc95d6ffe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Usamos el modo batch para SQLite
    with op.batch_alter_table("reparaciones_deas", schema=None) as batch_op:
        # Paso 1: Agregar nueva columna sin restricción unique
        batch_op.add_column(sa.Column("dea_id_help", sa.Integer, unique=False))

        # Paso 2: Copiar los datos (esto tendrás que hacerlo a través de una operación de tu app o manualmente)
        # op.execute('UPDATE reparaciones_deas SET dea_id_help = dea_id')

        # Paso 3: Eliminar la columna antigua
        batch_op.drop_column("dea_id")

        # Paso 4: Renombrar la nueva columna al nombre antiguo
        batch_op.alter_column("dea_id_help", new_column_name="dea_id")


def downgrade():
    # Comando para añadir la restricción unique a la columna dea_id
    pass
