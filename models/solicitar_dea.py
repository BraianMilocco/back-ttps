from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from db.base import Base


class SolicitudDea(Base):
    __tablename__ = "solicitudes_deas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.now())
    latitud = Column(String, index=True, nullable=False)
    longitud = Column(String, index=True, nullable=False)
    atendido = Column(Boolean, default=False)
    fecha_atendido = Column(DateTime, nullable=True)
    espacio_obligado_id = Column(
        Integer, ForeignKey("espacios_obligados.id"), nullable=False
    )
    espacio_obligado = relationship(
        "EspacioObligado", back_populates="solicitudes_deas"
    )
    dea_id = Column(Integer, ForeignKey("deas.id"), nullable=True)
    dea = relationship("Dea", back_populates="solicitudes_deas")
    responsable_sede_id = Column(
        Integer, ForeignKey("responsables_sedes.id"), nullable=True
    )
    responsable_sede = relationship(
        "ResponsableSede", back_populates="solicitudes_deas"
    )

    @classmethod
    def create(cls, data, espacio_id, db):
        solicitud = cls(
            latitud=data.latitud,
            longitud=data.longitud,
            espacio_obligado_id=espacio_id,
        )
        return cls.save(solicitud, db)

    def update(self, data, db):
        if not self.espacio_obligado.validar_dea(data.dea_id):
            return None, "La DEA no pertenece al espacio obligado"
        if not self.espacio_obligado.validar_responsable_sede(data.responsable_sede_id):
            return None, "El responsable de sede no pertenece al espacio obligado"
        self.atendido = data.atendido
        self.fecha_atendido = data.fecha_atendido
        self.dea_id = data.dea_id
        self.responsable_sede_id = data.responsable_sede_id

        try:
            db.commit()
            db.refresh(self)
        except Exception as e:
            db.rollback()
            return None, str(e)
        return self, None

    @classmethod
    def save(cls, solicitud, db):
        try:
            db.add(solicitud)
            db.commit()
            db.refresh(solicitud)
        except Exception as e:
            db.rollback()
            return None, str(e)
        return solicitud, None

    def to_dict_list(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "atendido": self.atendido,
            "fecha_atendido": self.fecha_atendido,
            "dea": self.dea.numero_serie if self.dea else None,
            "responsable_sede": self.responsable_sede.nombre
            if self.responsable_sede
            else None,
            "espacio_obligado": self.espacio_obligado.nombre
            if self.espacio_obligado
            else None,
        }

    @classmethod
    def get_by_espacio_obligado(cls, espacio_obligado_id, db):
        solicitudes = (
            db.query(cls).filter(cls.espacio_obligado_id == espacio_obligado_id).all()
        )
        data = []
        for solicitud in solicitudes:
            data.append(solicitud.to_dict_list())
        return data
