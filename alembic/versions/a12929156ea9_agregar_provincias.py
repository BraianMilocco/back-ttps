"""agregar provincias

Revision ID: a12929156ea9
Revises: 101639c2f1e0
Create Date: 2023-09-17 21:40:47.022728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# Agrega estos imports
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

# revision identifiers, used by Alembic.
revision: str = "a12929156ea9"
down_revision: Union[str, None] = "101639c2f1e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Define una referencia temporal a tu tabla para poder insertar datos
    provincia_table = table(
        "provincias",
        column("nombre", String),
        column("extension_km", Integer),
        column("poblacion", Integer),
    )

    # Inserta datos
    op.bulk_insert(
        provincia_table,
        [
            {"nombre": "Buenos Aires", "extension_km": 307571, "poblacion": 15625084},
            {"nombre": "Córdoba", "extension_km": 165321, "poblacion": 3308876},
            {"nombre": "Santa Fe", "extension_km": 133007, "poblacion": 3300730},
            {"nombre": "Mendoza", "extension_km": 148827, "poblacion": 1741610},
            {"nombre": "Tucumán", "extension_km": 22524, "poblacion": 1448188},
            {"nombre": "Entre Ríos", "extension_km": 78781, "poblacion": 1235994},
            {"nombre": "Salta", "extension_km": 155488, "poblacion": 1214441},
            {"nombre": "Chaco", "extension_km": 99633, "poblacion": 1055259},
            {"nombre": "Corrientes", "extension_km": 88199, "poblacion": 992595},
            {"nombre": "Misiones", "extension_km": 29801, "poblacion": 1097829},
            {"nombre": "San Juan", "extension_km": 89651, "poblacion": 680345},
            {"nombre": "Jujuy", "extension_km": 53219, "poblacion": 673307},
            {"nombre": "Río Negro", "extension_km": 203013, "poblacion": 638645},
            {"nombre": "Neuquén", "extension_km": 94078, "poblacion": 551266},
            {"nombre": "Formosa", "extension_km": 72066, "poblacion": 527895},
            {"nombre": "San Luis", "extension_km": 76748, "poblacion": 432310},
            {"nombre": "Catamarca", "extension_km": 102602, "poblacion": 367820},
            {"nombre": "La Rioja", "extension_km": 89680, "poblacion": 333642},
            {"nombre": "Chubut", "extension_km": 224686, "poblacion": 509108},
            {"nombre": "La Pampa", "extension_km": 143440, "poblacion": 318951},
            {"nombre": "Santa Cruz", "extension_km": 243943, "poblacion": 273964},
            {"nombre": "Tierra del Fuego", "extension_km": 21263, "poblacion": 127205},
            {
                "nombre": "Santiago del Estero",
                "extension_km": 136351,
                "poblacion": 874006,
            },
        ],
    )


def downgrade():
    # Si quisieras eliminar todas las provincias en una operación de downgrade
    op.execute("DELETE FROM provincias")
