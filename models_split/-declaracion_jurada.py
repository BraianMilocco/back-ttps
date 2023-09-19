from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db.base import Base


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
