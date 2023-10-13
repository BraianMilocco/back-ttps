from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from db.base import Base

# from .espacio_obligado import EspacioObligado
from .reparacion_dea import ReparacionDea
from .solicitar_dea import SolicitudDea


class Dea(Base):
    __tablename__ = "deas"

    id = Column(Integer, primary_key=True, index=True)
    numero_serie = Column(String, index=True, unique=True, nullable=False)
    nombre = Column(String, index=True, nullable=True)
    marca = Column(String, index=True, nullable=True)
    modelo = Column(String, index=True, nullable=True)
    solidario = Column(Boolean, default=False)
    activo = Column(Boolean, default=False)
    fecha_ultimo_mantenimiento = Column(DateTime, nullable=True)
    espacio_obligado_id = Column(
        Integer, ForeignKey("espacios_obligados.id"), nullable=False
    )
    espacio_obligado = relationship("EspacioObligado", back_populates="deas")
    reparaciones = relationship(ReparacionDea, back_populates="dea")
    solicitudes_deas = relationship(SolicitudDea, back_populates="dea")

    @classmethod
    def create(cls, data, db):
        dea = cls(
            numero_serie=data.numero_serie,
            nombre=data.nombre,
            marca=data.marca,
            modelo=data.modelo,
            solidario=data.solidario,
            activo=data.activo,
            fecha_ultimo_mantenimiento=data.fecha_ultimo_mantenimiento,
            espacio_obligado_id=data.espacio_obligado_id,
        )
        return cls.save(dea, db)

    @classmethod
    def save(cls, dea, db):
        try:
            db.add(dea)
            db.commit()
            db.refresh(dea)
        except Exception as e:
            db.rollback()
            return None, str(e)
        return dea, None

    def to_dict_list(self):
        return {
            "id": self.id,
            "numero_serie": self.numero_serie,
            "nombre": self.nombre,
            "marca": self.marca,
            "modelo": self.modelo,
            "solidario": self.solidario,
            "activo": self.activo,
            "fecha_ultimo_mantenimiento": self.fecha_ultimo_mantenimiento,
            "espacio_id": self.espacio_obligado_id,
        }

    @classmethod
    def get_by_espacio_obligado(cls, espacio_id, db):
        deas = db.query(cls).filter(cls.espacio_obligado_id == espacio_id).all()
        return [dea.to_dict_list() for dea in deas]

    @classmethod
    def get_by_id(cls, dea_id, db):
        return db.query(cls).filter(cls.id == dea_id).first()

    def update_activo(self, estado, db):
        self.activo = estado
        try:
            db.commit()
            db.refresh(self)
        except Exception as e:
            db.rollback()
            return None, str(e)
        return self, None

    def actualizar_fecha_ultimo_mantenimiento(self, db):
        self.fecha_ultimo_mantenimiento = datetime.now()
        try:
            db.commit()
            db.refresh(self)
        except Exception as e:
            db.rollback()
            return None, str(e)
        return self, None

    @classmethod
    def delete(cls, dea, db):
        try:
            db.delete(dea)
            db.commit()
        except Exception as e:
            db.rollback()
            return None, str(e)
        return True, None
