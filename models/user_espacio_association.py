from sqlalchemy import Column, Integer, ForeignKey, Table
from db.base import Base

# Tabla de asociación
user_espacio_association = Table(
    "user_espacio_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("espacio_id", Integer, ForeignKey("espacios_obligados.id")),
)
