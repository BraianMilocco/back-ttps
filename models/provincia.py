from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base
from models.sede import Sede


class Provincia(Base):
    __tablename__ = "provincias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    extension_km = Column(Integer, nullable=True)
    poblacion = Column(Integer, nullable=True)
    meses_duracion_certificado = Column(Integer, nullable=True)
    users = relationship("User", back_populates="provincia")
    sedes = relationship(Sede, back_populates="provincia")
