from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from db.base import Base

# from models.sede import Sede
from .dea import Dea
from .visita import Visita

# from .declaracion_jurada import DeclaracionJurada
from .muerte_subita import MuerteSubita
from .user_espacio_association import user_espacio_association

# from .espacio_user_asociation import espacio_user_association

ESTADOS = [
    "En proceso de ser Cardio-Asistido",
    "Cardio-Asistido con DDJJ",
    "Cardio-Asistido Certificado",
]


class EspacioObligado(Base):
    __tablename__ = "espacios_obligados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, unique=True, nullable=True)
    aprobado = Column(Boolean, default=True)
    estado = Column(
        String, index=True, nullable=True, default="en_proceso_de_ser_cardio_asistido"
    )
    sede_id = Column(Integer, ForeignKey("sedes.id"), nullable=False, unique=True)
    sede = relationship("Sede", back_populates="espacio_obligado", uselist=False)
    deas = relationship(Dea, back_populates="espacio_obligado")
    visitas = relationship(Visita, back_populates="espacio_obligado")
    muertes_subitas = relationship(MuerteSubita, back_populates="espacio_obligado")

    ddjj_personal_capacitado = Column(Boolean, nullable=True)
    ddjj_senaletica_adecuada = Column(Boolean, nullable=True)
    ddjj_protocolo_accion = Column(String, nullable=True)
    ddjj_sistema_energia_media = Column(String, nullable=True)
    ddjj_cantidad_deas = Column(Integer, nullable=True)

    administradores = relationship(
        "User",
        secondary=user_espacio_association,
        back_populates="espacios_administrados",
    )

    @property
    def declaracion_jurada(self):
        return {
            "personal_capacitado": self.ddjj_personal_capacitado,
            "senaletica_adecuada": self.ddjj_senaletica_adecuada,
            "protocolo_accion": self.ddjj_protocolo_accion,
            "sistema_energia_media": self.ddjj_sistema_energia_media,
            "cantidad_deas": self.ddjj_cantidad_deas,
        }

    # notificaciones = relationship("Notificacion", back_populates="espacio_obligado")

    __table_args__ = (CheckConstraint(estado.in_(ESTADOS)),)
