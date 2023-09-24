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

    @classmethod
    def create(cls, data, sede_id: int, db):
        responsable = cls(
            nombre=data.nombre,
            telefono=data.telefono,
            email=data.email,
            sede_id=sede_id,
        )

        return cls.save(responsable, db)

    @classmethod
    def save(cls, responsable, db):
        try:
            db.add(responsable)
            db.commit()
            return responsable, None
        except Exception as e:
            return None, str(e)

    @classmethod
    def get_by_sede(cls, sede_id: int, db):
        responsables = db.query(cls).filter(cls.sede_id == sede_id).all()
        lista = []
        for responsable in responsables:
            lista.append(responsable.get_dict())
        return lista

    def get_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email,
        }
