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
    dias_duracion_certificado = Column(Integer, nullable=True)
    users = relationship("User", back_populates="provincia")
    sedes = relationship(Sede, back_populates="provincia")

    @classmethod
    def get_all(cls, db):
        provincias = db.query(cls).all()
        return [provincia.to_dict_list() for provincia in provincias]

    def to_dict_list(self):
        return {"id": self.id, "nombre": self.nombre}

    @classmethod
    def get_id_from_nombre(cls, nombre, db):
        provincia = db.query(cls).filter(cls.nombre == nombre).first()
        return provincia.id if provincia else 1
