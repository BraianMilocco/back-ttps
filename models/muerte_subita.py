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

    @classmethod
    def create(cls, data, espacio_obligado_id, user_id, db):
        muerte_subita = cls(
            sexo=data.sexo,
            edad=data.edad,
            fallecio=data.fallecio,
            rcp=data.rcp,
            tiempo_rcp=data.tiempo_rcp,
            responsable_id=data.responsable_id,
            fecha=data.fecha,
            espacio_obligado_id=espacio_obligado_id,
            user_id=user_id,
        )
        return cls.save(muerte_subita, db)

    @classmethod
    def save(cls, muerte_subita, db):
        try:
            db.add(muerte_subita)
            db.commit()
            db.refresh(muerte_subita)
        except Exception as e:
            db.rollback()
            return None, str(e)
        return muerte_subita, None

    def to_dict_list(self):
        inconvenientes = (
            [i.to_dict() for i in self.incovenientes] if self.incovenientes else None
        )
        return {
            "id": self.id,
            "fecha": self.fecha,
            "sexo": self.sexo,
            "edad": self.edad,
            "fallecio": self.fallecio,
            "rcp": self.rcp,
            "tiempo_rcp": self.tiempo_rcp,
            "responsable_id": self.responsable_id,
            "incovenientes": inconvenientes,
            "espacio_obligado_id": self.espacio_obligado_id,
        }

    @classmethod
    def get_from_espacio(cls, espacio_id, db):
        muertes = db.query(cls).filter(cls.espacio_obligado_id == espacio_id).all()
        data = [muerte.to_dict_list() for muerte in muertes]
        return data

    @classmethod
    def get_from_id_and_espacio(cls, id, espacio_id, db):
        muerte = (
            db.query(cls)
            .filter(cls.id == id)
            .filter(cls.espacio_obligado_id == espacio_id)
            .first()
        )
        return muerte
