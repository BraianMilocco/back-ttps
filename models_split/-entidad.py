from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base

# from .user import User


class Entidad(Base):
    __tablename__ = "entidades"

    id = Column(Integer, primary_key=True, index=True)
    cuit = Column(String, unique=True, index=True, nullable=True)
    razon_social = Column(String, unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="entidades")
