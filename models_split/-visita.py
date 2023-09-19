from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from db.base import Base
from .espacio_obligado import EspacioObligado
from .user import User

RESULTADOS = ["Aprobado", "Rechazado", "Dado de baja"]


class Visita(Base):
    __tablename__ = "visitas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=True)
    observaciones = Column(String, index=True, nullable=True)
    resultado = Column(String, index=True, nullable=False)

    espacio_obligado_id = Column(
        Integer, ForeignKey("espacios_obligados.id"), nullable=True, unique=True
    )
    espacio_obligado = relationship(EspacioObligado, back_populates="visitas")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, unique=True)
    user = relationship(User, back_populates="visitas")

    __table_args__ = (CheckConstraint(resultado.in_(RESULTADOS)),)
