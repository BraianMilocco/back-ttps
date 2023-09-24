from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from db.base import Base


RESULTADOS = ["Aprobado", "Rechazado", "Dado de baja"]


class Visita(Base):
    __tablename__ = "visitas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, nullable=True)
    observaciones = Column(String, index=True, nullable=True)
    resultado = Column(String, index=True, nullable=False)

    espacio_obligado_id = Column(
        Integer,
        ForeignKey("espacios_obligados.id"),
        unique=False,
        nullable=True,
    )
    espacio_obligado = relationship("EspacioObligado", back_populates="visitas")
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=False,
        nullable=True,
    )
    user = relationship("User", back_populates="visitas")
    __table_args__ = (CheckConstraint(resultado.in_(RESULTADOS)),)

    @classmethod
    def create(cls, data, user_id, db):
        visita = cls(
            fecha=data.fecha,
            observaciones=data.observaciones,
            resultado=data.resultado,
            user_id=user_id,
            espacio_obligado_id=data.espacio_obligado,
        )
        return cls.save(visita, db)

    @classmethod
    def save(cls, visita, db):
        try:
            db.add(visita)
            db.commit()
            db.refresh(visita)
        except Exception as e:
            db.rollback()
            return None, str(e)
        return visita, None

    def paso(self):
        return self.resultado == "Aprobado"

    @classmethod
    def get_by_espacio_obligado(cls, espacio_obligado_id, db):
        visitas = (
            db.query(cls).filter(cls.espacio_obligado_id == espacio_obligado_id).all()
        )
        return [visita.to_dict_list() for visita in visitas]

    def to_dict_list(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "observaciones": self.observaciones,
            "resultado": self.resultado,
            "espacio_obligado_id": self.espacio_obligado_id,
            "espacio_obligado": self.espacio_obligado.nombre,
            "certificador": self.user.email,
        }

    @classmethod
    def get_all(cls, db):
        visitas = db.query(cls).all()
        return [visita.to_dict_list() for visita in visitas]
