from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from db.base import Base

# from .espacio_obligado import EspacioObligado


class Dea(Base):
    __tablename__ = "deas"

    id = Column(Integer, primary_key=True, index=True)
    numero_serie = Column(String, index=True, unique=True, nullable=False)
    nombre = Column(String, index=True, nullable=True)
    marca = Column(String, index=True, nullable=True)
    modelo = Column(String, index=True, nullable=True)
    solidario = Column(Boolean, default=False)
    activo = Column(Boolean, default=False)
    fecha_ultimo_mantenimiento = Column(DateTime, nullable=True)
    espacio_obligado_id = Column(
        Integer, ForeignKey("espacios_obligados.id"), nullable=False, unique=True
    )

    espacio_obligado = relationship("EspacioObligado", back_populates="deas")
    reparaciones = relationship("ReparacionDea", back_populates="dea")
