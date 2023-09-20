from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    CheckConstraint,
    DateTime,
)
from sqlalchemy.orm import relationship
from db.base import Base

from .incovenientes import Incovenientes

SEXOS = ["Masculino", "Femenino", "X"]


class MuerteSubita(Base):
    __tablename__ = "muertes_subitas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=True)
    sexo = Column(String, index=True, nullable=True)
    edad = Column(Integer, index=True, nullable=True)
    fallecio = Column(Boolean, default=False)
    rcp = Column(Boolean, default=False)
    tiempo_rcp = Column(Integer, index=True, nullable=True)

    incovenientes = relationship(Incovenientes, back_populates="muerte_subita")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="muertes_subitas")
    espacio_obligado_id = Column(
        Integer, ForeignKey("espacios_obligados.id"), nullable=False, unique=True
    )
    espacio_obligado = relationship("EspacioObligado", back_populates="muertes_subitas")
    responsable_id = Column(
        Integer, ForeignKey("responsables_sedes.id"), nullable=False, unique=True
    )
    responsable = relationship("ResponsableSede", back_populates="muertes_subitas")

    __table_args__ = (CheckConstraint(sexo.in_(SEXOS)),)
