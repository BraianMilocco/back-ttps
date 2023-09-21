from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
import re

from db.base import Base
from .provincia import Provincia
from .muerte_subita import MuerteSubita

from .user_espacio_association import user_espacio_association

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ROLES = [
    ("representante", "Representante"),
    ("administrador_provincial", "Administrador Provincial"),
    ("certificador", "Certificador"),
]


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # Relaciones
    provincia_id = Column(Integer, ForeignKey("provincias.id"), nullable=True)
    provincia = relationship(Provincia, back_populates="users")
    rol = Column(String, index=True)
    entidades = relationship("Entidad", back_populates="user")
    sedes = relationship("Sede", back_populates="user")
    visitas = relationship("Visita", back_populates="user")
    muertes_subitas = relationship(MuerteSubita, back_populates="user")

    espacios_administrados = relationship(
        "EspacioObligado",
        secondary=user_espacio_association,
        back_populates="administradores",
    )

    __tablename__ = "users"
    __table_args__ = (CheckConstraint(rol.in_([choice[0] for choice in ROLES])),)

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            return False
        elif not any(char.isdigit() for char in password):
            return False
        elif not any(char.isalpha() for char in password):
            return False
        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        return bool(email_pattern.match(email))

    @staticmethod
    def get_password_hash(password) -> str:
        return pwd_context.hash(password)

    @classmethod
    def create(cls, email: str, password: str, db):
        if not cls.validate_password(password):
            return (
                None,
                "La contraseña debe tener al menos 8 caracteres, una letra y un número",
            )
        if not cls.validate_email(email):
            return None, "El email no es válido"
        if cls.get_by_email(email, db):
            return None, "El email ya existe"
        hashed_password = pwd_context.hash(password)
        user = cls(email=email, hashed_password=hashed_password, rol="representante")
        return cls.save(user, db)

    @classmethod
    def save(cls, user, db):
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            print(e)
            return None, str(e)
        return user, None

    @classmethod
    def get_by_email(cls, email: str, db):
        return db.query(cls).filter(cls.email == email).first()

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def jwt_dict(self):
        return {
            "sub": self.email,
            "id": self.id,
            "rol": self.rol,
            "provincia": self.provincia.nombre if self.provincia else None,
        }
