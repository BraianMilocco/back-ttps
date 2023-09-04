from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String
from db.base import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @classmethod
    def create(cls, email: str, password: str, db):
        hashed_password = pwd_context.hash(password)
        user = cls(email=email, hashed_password=hashed_password)
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
