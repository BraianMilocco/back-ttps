from sqlalchemy import Column, Integer, ForeignKey, Table, Boolean
from db.base import Base
from db.session import SessionLocal

db = SessionLocal()

# Tabla de asociación
user_espacio_association = Table(
    "user_espacio_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("espacio_id", Integer, ForeignKey("espacios_obligados.id")),
    Column("valida", Boolean, default=False),
)


def get_administradores(espacio_id):
    return (
        db.query(user_espacio_association)
        .filter(user_espacio_association.c.valida == True)
        .filter(user_espacio_association.c.espacio_id == espacio_id)
        .all()
    )
