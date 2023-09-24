from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from db.base import Base


class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String, index=True, nullable=False)
    fecha = Column(DateTime, default=datetime.now())
    espacio_obligado_id = Column(
        Integer, ForeignKey("espacios_obligados.id"), nullable=False
    )
    espacio_obligado = relationship("EspacioObligado", back_populates="notificaciones")

    @classmethod
    def notificaciones_de_los_ultimos_dias(cls, espacios, db):
        fecha_limite = datetime.now() - timedelta(days=3)
        notificaciones = (
            db.query(cls)
            .filter(
                cls.espacio_obligado_id.in_(espacios),
                cls.fecha >= fecha_limite,
            )
            .all()
        )

        return [notificacion.to_dict_list() for notificacion in notificaciones]

    def to_dict_list(self):
        return {
            "id": self.id,
            "texto": self.texto,
            "fecha": self.fecha,
            "espacio_obligado_id": self.espacio_obligado_id,
            "espacio_obligado": self.espacio_obligado.nombre,
        }

    @classmethod
    def create(cls, text, espacio_id, db):
        notificacion = cls(texto=text, espacio_obligado_id=espacio_id)
        return cls.save(notificacion, db)

    @classmethod
    def save(cls, notificacion, db):
        try:
            db.add(notificacion)
            db.commit()
            db.refresh(notificacion)
        except Exception as e:
            db.rollback()
            return None, str(e)
        return notificacion, None
