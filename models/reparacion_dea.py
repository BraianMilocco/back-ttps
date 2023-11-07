from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base import Base


class ReparacionDea(Base):
    __tablename__ = "reparaciones_deas"

    id = Column(Integer, primary_key=True, index=True)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)
    tecnico = Column(String, index=True, nullable=True)
    dea_id = Column(Integer, ForeignKey("deas.id"), nullable=False, unique=False)
    dea = relationship("Dea", back_populates="reparaciones")

    @classmethod
    def create(cls, data, dea_id, db):
        reparacion_dea = cls(
            dea_id=dea_id,
            fecha_inicio=data.fecha_inicio,
            fecha_fin=data.fecha_fin,
            tecnico=data.tecnico,
        )
        return cls.save(reparacion_dea, db)

    @classmethod
    def save(cls, reparacion_dea, db):
        try:
            db.add(reparacion_dea)
            db.commit()
            db.refresh(reparacion_dea)
        except Exception as e:
            db.rollback()
            return None, str(e)
        return reparacion_dea, None

    def to_dict_list(self):
        return {
            "id": self.id,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "tecnico": self.tecnico,
            "dea_id": self.dea_id,
        }

    @classmethod
    def get_by_dea_dict(cls, dea_id, db):
        reparaciones = db.query(cls).filter(cls.dea_id == dea_id).all()
        reparaciones_list = []
        for reparacion in reparaciones:
            reparaciones_list.append(reparacion.to_dict_list())
        return reparaciones_list
