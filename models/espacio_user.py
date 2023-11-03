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


class EspacioUser(Base):
    __tablename__ = "espacio_user"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    espacio_id = Column(Integer, ForeignKey("espacios_obligados.id"), primary_key=True)
    valida = Column(Boolean, default=False)
    pendiente = Column(Boolean, default=True)
    user = relationship("User", back_populates="espacios")
    espacio = relationship("EspacioObligado", back_populates="users")
    fecha_creacion = Column(DateTime, nullable=True)

    @classmethod
    def get_by_user_and_espacio(cls, user_id, espacio_id, db):
        return (
            db.query(cls)
            .filter(cls.user_id == user_id, cls.espacio_id == espacio_id)
            .first()
        )

    @classmethod
    def create(cls, user_id, espacio_id, db, al_crear_espacio=False):
        if not al_crear_espacio:
            if cls.get_by_user_and_espacio(user_id, espacio_id, db):
                return (
                    None,
                    "El usuario ya es administrador o tiene una solicitud de este espacio",
                )
        espacio_user = cls(
            user_id=user_id,
            espacio_id=espacio_id,
            valida=False,
            fecha_creacion=datetime.now(),
        )
        return cls.save(espacio_user, db)

    @classmethod
    def save(cls, espacio_user, db, create=True):
        try:
            if create:
                db.add(espacio_user)
            db.commit()
            db.refresh(espacio_user)
        except Exception as e:
            db.rollback()
            print(e)
            return None, str(e)
        return espacio_user, None

    @classmethod
    def get_pending(cls, provincia_id, estado, db):
        solicitudes = db.query(cls)

        if estado == "APROBADO":
            solicitudes = solicitudes.filter(cls.valida == True).all()
        elif estado == "RECHAZADO":
            solicitudes = (
                solicitudes.filter(cls.pendiente == False)
                .filter(cls.valida == False)
                .all()
            )
        else:
            solicitudes = solicitudes.filter(cls.pendiente == True).all()

        lista_solicitudes = []
        for solicitud in solicitudes:
            if solicitud.espacio.sede.provincia_id == provincia_id:
                lista_solicitudes.append(solicitud.to_dict_list())
        return lista_solicitudes

    def to_dict_list(self):
        return {
            "espacio_id": self.espacio_id,
            "espacio_nombre": self.espacio.nombre,
            "pendiente": self.pendiente,
            "sede": self.espacio.sede.to_dict_list(),
            "user_id": self.user.id,
            "user": self.user.email,
            "creacion": self.fecha_creacion,
        }

    def update(self, db):
        try:
            db.commit()
            db.refresh(self)
        except Exception as e:
            db.rollback()
            print(e)
            return None, str(e)
        return self, None

    @classmethod
    def user_is_admin_sede(cls, user_id, sede_id, db):
        user_admins = (
            db.query(cls)
            .filter(cls.user_id == user_id)
            .filter(cls.pendiente == False)
            .all()
        )
        for user_admin in user_admins:
            if user_admin.valida == True and user_admin.espacio.sede_id == sede_id:
                return True
        return False

    @classmethod
    def user_is_admin_espacio(cls, user_id, espacio_id, db):
        user_admins = (
            db.query(cls)
            .filter(cls.user_id == user_id)
            .filter(cls.pendiente == False)
            .all()
        )
        for user_admin in user_admins:
            if user_admin.valida == True and user_admin.espacio_id == espacio_id:
                return True
        return False

    @classmethod
    def get_espacios_id_user_administra(cls, user_id, db):
        user_administra = (
            db.query(cls)
            .filter(cls.user_id == user_id)
            .filter(cls.pendiente == False)
            .filter(cls.valida == True)
            .order_by(cls.fecha_creacion.desc())
            .all()
        )
        return [user.espacio_id for user in user_administra] if user_administra else []

    def get_espacio(self):
        return self.espacio

    @classmethod
    def get_emails_admins_espacio(cls, espacio_id, db):
        admins = (
            db.query(cls)
            .filter(cls.espacio_id == espacio_id)
            .filter(cls.pendiente == False)
            .filter(cls.valida == True)
            .all()
        )
        return [admin.user.email for admin in admins] if admins else []
