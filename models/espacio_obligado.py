from datetime import datetime, timedelta
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

# from models.sede import Sede
from .dea import Dea
from .visita import Visita

# from .declaracion_jurada import DeclaracionJurada
from .muerte_subita import MuerteSubita
from .user_espacio_association import user_espacio_association
from .espacio_user import EspacioUser

ESTADOS = [
    "En proceso de ser Cardio-Asistido",
    "Cardio-Asistido con DDJJ",
    "Cardio-Asistido Certificado",
    "Cardio-Asisitdo Certificado Vencido",  # cuando se vence el certificado por provincia, fecha certificado + 1 año
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
    cardio_asistido_desde = Column(DateTime, nullable=True)
    cardio_asistido_vence = Column(DateTime, nullable=True)
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
    users = relationship(
        EspacioUser,
        back_populates="espacio",
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

    def to_dict_list(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "estado": self.estado,
            "aprobado": self.aprobado,
            "cant_administradores": len(self.admins()),
            "puede_completar_ddjj_dea": self.puede_completar_ddjj_dea,
            "cardio_asistido_desde": self.cardio_asistido_desde,
            "cardio_asistido_vence": self.cardio_asistido_vence,
        }

    def admins(self):
        return [user for user in self.users if user.valida]

    @property
    def puede_completar_ddjj_dea(self):
        return self.sede.info_completa()

    @classmethod
    def create(cls, espacio_obligado, user_id, db):
        espacio_obligado = cls(
            nombre=espacio_obligado.nombre,
            sede_id=espacio_obligado.sede_id,
            estado="En proceso de ser Cardio-Asistido",
        )
        return cls.save(espacio_obligado, db)

    @classmethod
    def save(cls, espacio_obligado, db):
        try:
            db.add(espacio_obligado)
            db.commit()
            db.refresh(espacio_obligado)
        except Exception as e:
            db.rollback()
            print(e)
            return None, str(e)
        return espacio_obligado, None

    def solicitar_administracion(self, user, db):
        self.administradores.append(user)
        try:
            db.commit()
            db.refresh(self)
        except Exception as e:
            db.rollback()
            print(e)
            return None, str(e)
        return self, None

    @classmethod
    def tiene_jurisdiccion(cls, espacio_obligado_id, provincia_id, db):
        espacio = db.query(cls).filter(cls.id == espacio_obligado_id).first()
        if not espacio:
            return False, "No existe el espacio obligado"
        if not espacio.sede.provincia_id == provincia_id:
            return False, "No tiene jurisdiccion en esta Provincia"
        return True, None

    @classmethod
    def get_by_id(cls, espacio_obligado_id, db):
        return db.query(cls).filter(cls.id == espacio_obligado_id).first()

    def certificar(self, db):
        self.estado = "Cardio-Asistido Certificado"
        self.cardio_asistido_desde = datetime.now()
        self.cardio_asistido_vence = datetime.now() + timedelta(
            days=self.sede.provincia.dias_duracion_certificado
        )
        try:
            db.commit()
            db.refresh(self)
        except Exception as e:
            db.rollback()
            print(e)
            return None, "error al certificar el espacio obligado"
        return self, None
