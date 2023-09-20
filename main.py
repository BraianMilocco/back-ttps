from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from db.base import Base
from db.session import SessionLocal, engine
from models.user import User
from helpers import create_access_token, get_data_from_token
from settings import settings
from schemas.user import UserCreate, UserLogin
from schemas.espacios_obligados import AprobarEspacioObligado

app = FastAPI()

tokenUrl = "/users/login"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=tokenUrl)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se pudo validar credenciales",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return get_data_from_token(payload)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
            headers={"WWW-Authenticate": "Bearer"},
        )


def user_has_role(user: dict, rol: str) -> bool:
    if not user["rol"] == rol:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permiso Denegado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/")
def create_user(user_data: UserLogin, db: Session = Depends(get_db)):
    user, message = User.create(
        email=user_data.email, password=user_data.password, db=db
    )
    if not user:
        return {"success": False, "message": message}
    return {"success": True, "email": user.email, "id": user.id}


@app.post("/users/login")
def login_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = User.get_by_email(email=user_data.email, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not User.verify_password(
        plain_password=user_data.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token = create_access_token(data=user.jwt_dict())
    return {"success": True, "access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user


@app.post("/espacios_obligados/")
async def aprobar(
    aprobado: AprobarEspacioObligado, current_user: dict = Depends(get_current_user)
):
    user_has_role(current_user, "administrador_provincial")
    if aprobado.aprobado:
        return {"success": True, "message": "Administracion aprobada"}
    return {"success": False, "message": "Administracion rechazada"}


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")
