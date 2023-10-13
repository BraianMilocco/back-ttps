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
from datetime import datetime

# from models.sede import Sede
from .dea import Dea
from .visita import Visita

# from .declaracion_jurada import DeclaracionJurada
from .muerte_subita import MuerteSubita
from .user_espacio_association import user_espacio_association
from .espacio_user import EspacioUser
from .notificacion import Notificacion

ESTADOS = [
    "En proceso de ser Cardio-Asistido",
    "Cardio-Asistido con DDJJ",
    "Cardio-Asistido Certificado",
    # "Cardio-Asistido Certificado Vencido",  # cuando se vence el certificado por provincia, fecha certificado + 1 año
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
    visitas = relationship(Visita, back_populates="espacio_obligado")
    muertes_subitas = relationship(MuerteSubita, back_populates="espacio_obligado")
    notificaciones = relationship(Notificacion, back_populates="espacio_obligado")
    cardio_asistido_desde = Column(DateTime, nullable=True)
    cardio_asistido_vence = Column(DateTime, nullable=True)
    cardio_asistido_vencido = Column(Boolean, nullable=True, default=False)
    deas = relationship(Dea, back_populates="espacio_obligado")
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

    def to_dict_user_list(self, user_id):
        espacio_obligado = self.to_dict_list()
        espacio_obligado["solicitado"] = len(self.user_solicitudes(user_id))
        espacio_obligado["sede"] = self.sede.to_dict_list()
        return espacio_obligado

    def to_dict_list(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "estado": self.get_estado,
            "aprobado": self.aprobado,
            "cant_administradores": len(self.admins()),
            "puede_cargar_dea": self.sede.info_completa(),
            "puede_completar_ddjj_dea": self.puede_completar_ddjj_dea,
            "cardio_asistido_desde": self.cardio_asistido_desde,
            "cardio_asistido_vence": self.cardio_asistido_vence,
            "ddjj": self.ddjj_dict,
        }

    @property
    def ddjj_dict(self):
        return {
            "personal_capacitado": self.ddjj_personal_capacitado,
            "senaletica_adecuada": self.ddjj_senaletica_adecuada,
            "protocolo_accion": self.ddjj_protocolo_accion,
            "sistema_energia_media": self.ddjj_sistema_energia_media,
            "cantidad_deas": self.ddjj_cantidad_deas,
            "cantidad_deas_cargados": len(self.deas) if self.deas else 0,
        }

    @property
    def get_estado(self):
        if self.estado == "Cardio-Asistido Certificado":
            if self.cardio_asistido_vencido:
                return "Cardio-Asistido Certificado Vencido"
        return self.estado

    def user_solicitudes(self, user_id):
        return [user.user_id for user in self.users if user.user_id == user_id]

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
            cardio_asistido_vencido=False,
        )
        espacio, message = cls.save(espacio_obligado, db)
        if espacio:
            Notificacion.create(
                f"Se creo el espacio obligado {espacio.nombre}", espacio.id, db
            )
        return espacio, message

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

    @classmethod
    def get_by_sede_id(cls, sede_id, db):
        return db.query(cls).filter(cls.sede_id == sede_id).first()

    def certificar(self, db):
        self.estado = "Cardio-Asistido Certificado"
        self.cardio_asistido_desde = datetime.now()
        self.cardio_asistido_vence = datetime.now() + timedelta(
            days=self.sede.provincia.dias_duracion_certificado
        )
        self.cardio_asistido_vencido = False
        try:
            db.commit()
            db.refresh(self)
        except Exception as e:
            db.rollback()
            print(e)
            return None, "error al certificar el espacio obligado"
        Notificacion.create(
            f"Se certifico el espacio obligado {self.nombre}", self.id, db
        )
        return self, None

    def cardio_asistido_con_ddjj(self):
        if self.estado in [
            "Cardio-Asistido Certificado",
            "Cardio-Asistido Certificado Vencido",
        ]:
            return False
        len_deas = len(self.deas) if self.deas else 0
        return (
            self.ddjj_personal_capacitado
            and self.ddjj_senaletica_adecuada
            and len_deas > 0
            and len_deas == self.ddjj_cantidad_deas
        )

    def validar_ddjj(self, db):
        if not self.cardio_asistido_con_ddjj():
            if self.estado == "Cardio-Asistido con DDJJ":
                self.estado = "En proceso de ser Cardio-Asistido"
                self.cardio_asistido_vencido = False
            else:
                return True, None
        else:
            self.estado = "Cardio-Asistido con DDJJ"
            self.cardio_asistido_vencido = False
        try:
            db.commit()
            db.refresh(self)
        except Exception as e:
            db.rollback()
            return (
                None,
                "Se cargo la ddj pero no se pudo actualizar el estado a Cardio-Asistido con DDJJ",
            )
        Notificacion.create(
            f"Se cambio el estado del espacio obligado a {self.estado}", self.id, db
        )
        return self, None

    def update_ddjj(self, ddjj, db):
        estado_cambiado = False
        self.ddjj_personal_capacitado = ddjj.personal_capacitado
        self.ddjj_senaletica_adecuada = ddjj.senaletica_adecuada
        self.ddjj_protocolo_accion = ddjj.protocolo_accion
        self.ddjj_sistema_energia_media = ddjj.sistema_energia_media
        self.ddjj_cantidad_deas = ddjj.cantidad_deas
        if self.cardio_asistido_con_ddjj():
            estado_cambiado = True
            mensaje_notificacion = (
                "Se completo la ddjj y se cambio el estado a Cardio-Asistido con DDJJ"
            )
            self.estado = "Cardio-Asistido con DDJJ"
            self.cardio_asistido_vencido = False
        else:
            if self.estado == "Cardio-Asistido con DDJJ":
                estado_cambiado = True
                mensaje_notificacion = "El estado paso a En proceso de ser Cardio-Asistido por incongruencias ddjj y deas"
                self.estado = "En proceso de ser Cardio-Asistido"
                self.cardio_asistido_vencido = False
        try:
            db.commit()
            db.refresh(self)
        except Exception as e:
            db.rollback()
            print(e)
            return None, "error al cargar la ddjj"
        if estado_cambiado:
            Notificacion.create(mensaje_notificacion, self.id, db)
        return self, None

    def certificado_vencido(self):
        if not self.estado == "Cardio-Asistido Certificado":
            return False
        return datetime.now() > self.cardio_asistido_vence

    def vencer_certificado(self, db):
        self.estado = "Cardio-Asistido Certificado"
        self.cardio_asistido_desde = None
        self.cardio_asistido_vence = None
        self.cardio_asistido_vencido = True
        try:
            db.commit()
            db.refresh(self)
        except Exception as e:
            db.rollback()
            print(e)
            return None, "error al cambiar estado"
        Notificacion.create(
            f"Se vencio el certificado del espacio obligado {self.nombre}", self.id, db
        )
        return self, None

    @classmethod
    def get_cardioasistidos_certificados(cls, db):
        return db.query(cls).filter(cls.estado == "Cardio-Asistido Certificado").all()

    def certificar_vencido(self, db):
        self.estado = "Cardio-Asistido Certificado"
        self.cardio_asistido_desde = datetime.now() - timedelta(days=10)
        self.cardio_asistido_vence = datetime.now() - timedelta(days=5)
        self.cardio_asistido_vencido = False
        try:
            db.commit()
            db.refresh(self)
        except Exception as e:
            db.rollback()
            print(e)
            return None, "error al cambiar estado"
        Notificacion.create(
            f"Se Cambio via admin el estado y la fecha del certificado {self.nombre}",
            self.id,
            db,
        )
        return self, None

    @classmethod
    def get_vencidos(cls, db):
        """recupera los espacios con estado 'Cardio-Asistido Certificado' cuya fecha de vencimiento es mas chica a hoy"""
        return (
            db.query(cls)
            .filter(cls.estado == "Cardio-Asistido Certificado")
            .filter(cls.cardio_asistido_vence < datetime.now())
            .all()
        )

    def to_dict_public(self):
        deas = [dea.to_dict_list() for dea in self.deas] if self.deas else None
        return {
            "id": self.id,
            "nombre": self.nombre,
            "estado": self.get_estado,
            "aprobado": self.aprobado,
            "cant_administradores": len(self.admins()),
            "cardio_asistido_desde": self.cardio_asistido_desde,
            "cardio_asistido_vence": self.cardio_asistido_vence,
            "deas": deas,
            "latitud": self.sede.latitud,
            "longitud": self.sede.longitud,
        }
