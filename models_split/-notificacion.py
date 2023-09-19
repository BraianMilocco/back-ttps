from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from db.base import Base

# from .espacio_obligado import EspacioObligado


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    leida = Column(Boolean, default=False)
    nombre_espacio_obligado = Column(String, index=True, nullable=True)
    fecha = Column(DateTime, nullable=True)
    viejo_estado = Column(String, index=True, nullable=True)
    nuevo_estado = Column(String, index=True, nullable=True)
    extra_info = Column(String, index=True, nullable=True)
    espacio_obligado_id = Column(
        Integer, ForeignKey("espacios_obligados.id"), nullable=True, unique=True
    )
    espacio_obligado = relationship("EspacioObligado", back_populates="notifaciones")
