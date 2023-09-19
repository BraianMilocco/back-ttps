from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base import Base

# from .dea import Dea


class ReparacionDea(Base):
    __tablename__ = "reparaciones_deas"

    id = Column(Integer, primary_key=True, index=True)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)
    tecnico = Column(String, index=True, nullable=True)
    dea_id = Column(Integer, ForeignKey("deas.id"), nullable=False, unique=True)
    dea = relationship("Dea", back_populates="reparaciones")
