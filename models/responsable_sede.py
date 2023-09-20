from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

# from .sede import Sede
from .muerte_subita import MuerteSubita


class ResponsableSede(Base):
    __tablename__ = "responsables_sedes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=True)
    telefono = Column(String, index=True, nullable=True)
    email = Column(String, index=True, nullable=True)

    sede_id = Column(Integer, ForeignKey("sedes.id"), nullable=False)
    sede = relationship("Sede", back_populates="responsables")
    muertes_subitas = relationship(MuerteSubita, back_populates="responsable")
