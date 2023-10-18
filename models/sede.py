from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from db.base import Base

# from .user import User
# from .provincia import Provincia
from .espacio_obligado import EspacioObligado
from .entidad import Entidad
from .responsable_sede import ResponsableSede

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
    provincia_id = Column(Integer, ForeignKey("provincias.id"), nullable=False)
    provincia = relationship("Provincia", back_populates="sedes")
    entidad_id = Column(Integer, ForeignKey("entidades.id"), nullable=False)
    entidad = relationship(Entidad, back_populates="sedes")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="sedes")
    espacio_obligado = relationship(EspacioObligado, back_populates="sede")
    responsables = relationship(ResponsableSede, back_populates="sede")

    __table_args__ = (
        CheckConstraint(sector.in_([choice[0] for choice in SECTORES])),
        UniqueConstraint("numero", "entidad_id", name="uq_numero_entidad"),
    )

    def to_dict_list(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "direccion": self.direccion,
            "sector": self.sector,
            "provincia_id": self.provincia_id,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "superficie": self.superficie,
            "cantidad_pisos": self.cantidad_pisos,
            "cantidad_personas_externas": self.cantidad_personas_externas,
            "cantidad_personas_estables": self.cantidad_personas_estables,
            "espacio_obligado": self.espacio_obligado[0].to_dict_list()["id"]
            if self.espacio_obligado
            else None,
            "entidad": {
                "id": self.entidad_id,
                "cuit": self.entidad.cuit,
                "razon_social": self.entidad.razon_social,
            },
        }

    def info_completa(self):
        if (
            self.sector
            and self.tipo
            and self.direccion
            and self.latitud
            and self.longitud
            and self.superficie is not None
            and self.cantidad_pisos is not None
            and self.cantidad_personas_externas is not None
            and self.cantidad_personas_estables is not None
            and len(self.responsables) > 0
        ):
            return True
        return False

    def get_espacio_obligado(self):
        if self.espacio_obligado:
            return self.espacio_obligado[0]
        return None

    @classmethod
    def save(cls, sede, db):
        try:
            db.add(sede)
            db.commit()
            db.refresh(sede)
        except Exception as e:
            db.rollback()
            print(e)
            return None, str(e)
        return sede, None

    @classmethod
    def create(cls, sede, user_id, db):
        sede = cls(
            nombre=sede.nombre,
            numero=sede.numero,
            direccion=sede.direccion,
            provincia_id=sede.provincia_id,
            entidad_id=sede.entidad_id,
            user_id=user_id,
        )
        return cls.save(sede, db)

    @classmethod
    def get_by_id(cls, sede_id, db):
        return db.query(cls).filter(cls.id == sede_id).first()

    def update(self, data, db):
        self.sector = data.sector
        self.tipo = data.tipo
        self.superficie = data.superficie
        self.latitud = data.latitud
        self.longitud = data.longitud
        self.cantidad_pisos = data.cantidad_pisos
        self.cantidad_personas_externas = data.cantidad_personas_externas
        self.cantidad_personas_estables = data.cantidad_personas_estables

        try:
            db.commit()
            db.refresh(self)
        except Exception as e:
            db.rollback()
            print(e)
            return None, str(e)
        return self, None

    @classmethod
    def get_by_provincia(cls, provincia_id, db):
        return db.query(cls).filter(cls.provincia_id == provincia_id).all()

    def list_deas(self):
        if self.espacio_obligado:
            return [dea.to_dict_list() for dea in self.espacio_obligado[0].deas]
        return []

    def list_espacios(self, lat=None, lon=None):
        if self.espacio_obligado:
            return [
                espacio.to_dict_public(lat, lon) for espacio in self.espacio_obligado
            ]
        return []

    def validar_responsable_sede(self, responsable_sede_id):
        for responsable in self.responsables:
            if responsable.id == responsable_sede_id:
                return True
        return False
