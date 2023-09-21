from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from db.base import Base

# from .user import User
# from .provincia import Provincia
from .espacio_obligado import EspacioObligado
from .entidad import Entidad
from .responsable_sede import ResponsableSede

SECTORES = [
    ("publico", "Público"),
    ("privado", "Privado"),
]


class Sede(Base):
    __tablename__ = "sedes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    numero = Column(Integer, index=True, nullable=False)
    sector = Column(String, index=True, nullable=True)
    tipo = Column(String, index=True, nullable=True)
    direccion = Column(String, index=True, nullable=True)
    latitud = Column(String, index=True, nullable=True)
    longitud = Column(String, index=True, nullable=True)
    superficie = Column(Integer, index=True, nullable=True)
    cantidad_pisos = Column(Integer, index=True, nullable=True)
    cantidad_personas_externas = Column(Integer, index=True, nullable=True)
    cantidad_personas_estables = Column(Integer, index=True, nullable=True)
    provincia_id = Column(Integer, ForeignKey("provincias.id"), nullable=False)
    provincia = relationship("Provincia", back_populates="sedes")
    entidad_id = Column(Integer, ForeignKey("entidades.id"), nullable=False)
    entidad = relationship(Entidad, back_populates="sedes")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="sedes")
    espacio_obligado = relationship(EspacioObligado, back_populates="sede")
    responsables = relationship(ResponsableSede, back_populates="sede")

    __table_args__ = (
        CheckConstraint(sector.in_([choice[0] for choice in SECTORES])),
        UniqueConstraint("numero", "entidad_id", name="uq_numero_entidad"),
    )

    def to_dict_list(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "sector": self.sector,
            "espacio_obligado": self.espacio_obligado[0].to_dict_list()
            if self.espacio_obligado
            else None,
        }

    @classmethod
    def save(cls, sede, db):
        try:
            db.add(sede)
            db.commit()
            db.refresh(sede)
        except Exception as e:
            db.rollback()
            print(e)
            return None, str(e)
        return sede, None

    @classmethod
    def create(cls, sede, user_id, db):
        sede = cls(
            nombre=sede.nombre,
            numero=sede.numero,
            sector=sede.sector,
            direccion=sede.direccion,
            latitud=sede.latitud,
            longitud=sede.longitud,
            provincia_id=sede.provincia_id,
            entidad_id=sede.entidad_id,
            user_id=user_id,
        )
        return cls.save(sede, db)
