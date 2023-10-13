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

    @classmethod
    def create(cls, data, muerte_subita_id, db):
        inconveniente = cls(
            muerte_subita_id=muerte_subita_id,
            fecha=data.fecha,
            falta_insumos=data.falta_insumos,
            estaba_en_sitio=data.estaba_en_sitio,
            respondio_con_descargas_electricas=data.respondio_con_descargas_electricas,
            cantidad_de_descargas=data.cantidad_de_descargas,
            extra_info=data.extra_info,
        )
        return cls.save(inconveniente, db)

    @classmethod
    def save(cls, inconveniente, db):
        try:
            db.add(inconveniente)
            db.commit()
            db.refresh(inconveniente)
        except Exception as e:
            db.rollback()
            return None, str(e)
        return inconveniente, None

    def to_dict_list(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "falta_insumos": self.falta_insumos,
            "estaba_en_sitio": self.estaba_en_sitio,
            "respondio_con_descargas_electricas": self.respondio_con_descargas_electricas,
            "cantidad_de_descargas": self.cantidad_de_descargas,
            "extra_info": self.extra_info,
            "muerte_subita_id": self.muerte_subita_id,
        }
