from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship
from db.base import Base


class Incovenientes(Base):
    __tablename__ = "incovenientes"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=True)
    falta_insumos = Column(Boolean, default=False)
    estaba_en_sitio = Column(Boolean, default=False)
    respondio_con_descargas_electricas = Column(Boolean, default=False)
    cantidad_de_descargas = Column(Integer, index=True, nullable=True)
    extra_info = Column(String, index=True, nullable=True)

    muerte_subita_id = Column(
        Integer, ForeignKey("muertes_subitas.id"), nullable=False, unique=True
    )
    muerte_subita = relationship("MuerteSubita", back_populates="incovenientes")
