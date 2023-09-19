from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from db.base import Base

# from .declaracion_jurada import DeclaracionJurada

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
    deas = relationship("Dea", back_populates="espacio_obligado")
    visitas = relationship("Visita", back_populates="espacio_obligado")
    # declaracion_jurada_id = Column(
    #     Integer, ForeignKey("declaraciones_juradas.id"), nullable=True, unique=True
    # )
    # declaracion_jurada = relationship(
    #     "DeclaracionJurada", back_populates="espacio_obligado", uselist=False
    # )

    # notificaciones = relationship("Notificacion", back_populates="espacio_obligado")

    # administradores = relationship(
    #     "User", secondary=espacio_user_association, back_populates="espacios"
    # )

    __table_args__ = (CheckConstraint(estado.in_(ESTADOS)),)
