from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from db.base import Base

from .user import User
from .provincia import Provincia
from .entidad import Entidad


SECTORES = [
    ("publico", "Público"),
    ("privado", "Privado"),
]


class Sede(Base):
    __tablename__ = "sedes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    numero = Column(Integer, index=True, nullable=False)
    sector = Column(String, index=True, nullable=True)
    tipo = Column(String, index=True, nullable=True)
    direccion = Column(String, index=True, nullable=True)
    latitud = Column(String, index=True, nullable=True)
    longitud = Column(String, index=True, nullable=True)
    superficie = Column(Integer, index=True, nullable=True)
    cantidad_pisos = Column(Integer, index=True, nullable=True)
    cantidad_personas_externas = Column(Integer, index=True, nullable=True)
    cantidad_personas_estables = Column(Integer, index=True, nullable=True)

    entidad_id = Column(Integer, ForeignKey("entidades.id"), nullable=False)
    entidad = relationship(Entidad, back_populates="sedes")
    provincia_id = Column(Integer, ForeignKey("provincias.id"), nullable=False)
    provincia = relationship(Provincia, back_populates="sedes")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship(User, back_populates="entidades")

    responsables = relationship("ResponsableSede", back_populates="sede")

    __table_args__ = (
        CheckConstraint(sector.in_([choice[0] for choice in SECTORES])),
        UniqueConstraint("numero", "entidad_id", name="uq_numero_entidad"),
    )
