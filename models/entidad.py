from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class Entidad(Base):
    __tablename__ = "entidades"

    id = Column(Integer, primary_key=True, index=True)
    cuit = Column(String, unique=True, index=True, nullable=True)
    razon_social = Column(String, unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="entidades")
    sedes = relationship("Sede", back_populates="entidad")

    @classmethod
    def get_all(cls, db):
        entidades = db.query(cls).all()
        return [entidad.to_dict_list() for entidad in entidades]

    def to_dict_list(self):
        sedes = [sede.to_dict_list() for sede in self.sedes] if self.sedes else None
        return {
            "id": self.id,
            "cuit": self.cuit,
            "razon_social": self.razon_social,
            "sedes": sedes,
        }

    @classmethod
    def create(cls, entidad, user_id, db):
        entidad = cls(
            cuit=entidad.cuit,
            razon_social=entidad.razon_social,
            user_id=user_id,
        )
        return cls.save(entidad, db)

    @classmethod
    def save(cls, entidad, db):
        try:
            db.add(entidad)
            db.commit()
            db.refresh(entidad)
        except Exception as e:
            db.rollback()
            print(e)
            return None, str(e)
        return entidad, None

    @classmethod
    def get_by_id(cls, entidad_id, db):
        return db.query(cls).filter(cls.id == entidad_id).first()
