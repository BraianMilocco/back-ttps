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


class UserEspacioAssociation(Base):
    __tablename__ = "espacio_user"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    espacio_id = Column(Integer, ForeignKey("espacios_obligados.id"), primary_key=True)
    valida = Column(Boolean, default=False)
