from passlib.context import CryptContext
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    Boolean,
    DateTime,
)
from sqlalchemy.orm import relationship
import re

from db.base import Base


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User:
    pass


class Provincia:
    pass


class Sede:
    pass


class EspacioObligado:
    pass


class DeclaracionJurada:
    pass


class Dea:
    pass


class ResponsableSede:
    pass


class MuerteSubita:
    pass


class Incovenientes:
    pass


class Notificacion:
    pass


class Visita:
    pass


class ReparacionDea:
    pass


class Entidad:
    pass


ROLES = [
    ("representante", "Representante"),
    ("administrador_provincial", "Administrador Provincial"),
    ("certificador", "Certificador"),
]


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    provincia_id = Column(Integer, ForeignKey("provincias.id"), nullable=True)
    provincia = relationship("Provincia", back_populates="users")
    rol = Column(String, index=True)
    entidades = relationship("Entidad", back_populates="user")

    visitas = relationship("Visita", back_populates="user")
    # espacios = relationship(
    #     "EspacioObligado",
    #     secondary=espacio_user_association,
    #     back_populates="administradores",
    # )
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
        print("get_by_email")
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


class Provincia(Base):
    __tablename__ = "provincias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    extension_km = Column(Integer, nullable=True)
    poblacion = Column(Integer, nullable=True)

    users = relationship("User", back_populates="provincia")
    sedes = relationship("Sede", back_populates="provincia")


class Entidad(Base):
    __tablename__ = "entidades"

    id = Column(Integer, primary_key=True, index=True)
    cuit = Column(String, unique=True, index=True, nullable=True)
    razon_social = Column(String, unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="entidades")
    sedes = relationship("Sede", back_populates="entidad")


SECTORES = [
    ("publico", "Público"),
    ("privado", "Privado"),
]


class Sede(Base):
    __tablename__ = "sedes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    numero = Column(Integer, index=True, nullable=False)
    sector = Column(String, index=True, nullable=True)
    tipo = Column(String, index=True, nullable=True)
    direccion = Column(String, index=True, nullable=True)
    latitud = Column(String, index=True, nullable=True)
    longitud = Column(String, index=True, nullable=True)
    superficie = Column(Integer, index=True, nullable=True)
    cantidad_pisos = Column(Integer, index=True, nullable=True)
    cantidad_personas_externas = Column(Integer, index=True, nullable=True)
    cantidad_personas_estables = Column(Integer, index=True, nullable=True)

    entidad_id = Column(Integer, ForeignKey("entidades.id"), nullable=False)
    entidad = relationship("Entidad", back_populates="sedes")
    provincia_id = Column(Integer, ForeignKey("provincias.id"), nullable=False)
    provincia = relationship("Provincia", back_populates="sedes")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="entidades")

    responsables = relationship("ResponsableSede", back_populates="sedes")
    espacio_obligado = relationship(
        "EspacioObligado", back_populates="sede", uselist=False
    )

    __table_args__ = (
        CheckConstraint(sector.in_([choice[0] for choice in SECTORES])),
        UniqueConstraint("numero", "entidad_id", name="uq_numero_entidad"),
    )


ESTADOS = [
    "En proceso de ser Cardio-Asistido",
    "Cardio-Asistido con DDJJ",
    "Cardio-Asistido Certificado",
]


class EspacioObligado(Base):
    __tablename__ = "espacios_obligados"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, unique=True, nullable=True)
    aprobado = Column(Boolean, default=False)
    estado = Column(
        String, index=True, nullable=True, default="en_proceso_de_ser_cardio_asistido"
    )
    sede_id = Column(Integer, ForeignKey("sedes.id"), nullable=False, unique=True)
    sede = relationship(Sede, back_populates="espacio_obligado", uselist=False)
    declaracion_jurada_id = Column(
        Integer, ForeignKey("declaraciones_juradas.id"), nullable=True, unique=True
    )
    declaracion_jurada = relationship(
        "DeclaracionJurada", back_populates="espacio_obligado", uselist=False
    )
    deas = relationship("Dea", back_populates="espacio_obligado")
    notificaciones = relationship("Notificacion", back_populates="espacio_obligado")

    visitas = relationship("Visita", back_populates="espacio_obligado")

    # administradores = relationship(
    #     "User", secondary=espacio_user_association, back_populates="espacios"
    # )

    __table_args__ = (CheckConstraint(estado.in_(ESTADOS)),)


class DeclaracionJurada(Base):
    __tablename__ = "declaraciones_juradas"

    id = Column(Integer, primary_key=True, index=True)
    personal_capacitado = Column(Boolean, default=False)
    senaletica_adecuada = Column(Boolean, default=False)
    protocolo_accion = Column(String)
    sistema_energia_media = Column(String)
    cantidad_deas = Column(Integer)

    espacio_obligado = relationship(
        "EspacioObligado", back_populates="declaracion_jurada", uselist=False
    )


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
        Integer, ForeignKey("espacios_obligados.id"), nullable=False, unique=True
    )

    espacio_obligado = relationship("EspacioObligado", back_populates="deas")
    reparaciones = relationship("ReparacionDea", back_populates="dea")


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

    incovenientes = relationship("Incovenientes", back_populates="muerte_subita")
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


class ResponsableSede(Base):
    __tablename__ = "responsables_sedes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=True)
    telefono = Column(String, index=True, nullable=True)
    email = Column(String, index=True, nullable=True)

    sede_id = Column(Integer, ForeignKey("sedes.id"), nullable=False)
    sede = relationship("Sede", back_populates="responsables")

    muertes_subitas = relationship("MuerteSubita", back_populates="responsable_sede")


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    leida = Column(Boolean, default=False)
    nombre_espacio_obligado = Column(String, index=True, nullable=True)
    fecha = Column(DateTime, nullable=True)
    viejo_estado = Column(String, index=True, nullable=True)
    nuevo_estado = Column(String, index=True, nullable=True)
    extra_info = Column(String, index=True, nullable=True)
    espacio_obligado_id = Column(
        Integer, ForeignKey("espacios_obligados.id"), nullable=True, unique=True
    )
    espacio_obligado = relationship("EspacioObligado", back_populates="notifaciones")


RESULTADOS = ["Aprobado", "Rechazado", "Dado de baja"]


class Visita(Base):
    __tablename__ = "visitas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=True)
    observaciones = Column(String, index=True, nullable=True)
    resultado = Column(String, index=True, nullable=False)

    espacio_obligado_id = Column(
        Integer, ForeignKey("espacios_obligados.id"), nullable=True, unique=True
    )
    espacio_obligado = relationship(EspacioObligado, back_populates="visitas")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, unique=True)
    user = relationship(User, back_populates="visitas")

    __table_args__ = (CheckConstraint(resultado.in_(RESULTADOS)),)


class ReparacionDea(Base):
    __tablename__ = "reparaciones_deas"

    id = Column(Integer, primary_key=True, index=True)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)
    tecnico = Column(String, index=True, nullable=True)
    dea_id = Column(Integer, ForeignKey("deas.id"), nullable=False, unique=True)
    dea = relationship("Dea", back_populates="reparaciones")
