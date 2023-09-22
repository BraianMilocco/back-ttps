from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from db.base import Base
from db.session import SessionLocal, engine
from settings import settings

# Helpers
from helpers import create_access_token, get_data_from_token

# Schemas
from schemas.user import UserCreate, UserLogin
from schemas.espacios_obligados import EspacioObligado as EspacioObligadoSchema
from schemas.entidad import Entidad as EntidadSchema
from schemas.sede import Sede as SedeSchema

# Models
from models.user import User
from models.entidad import Entidad
from models.provincia import Provincia
from models.sede import Sede
from models.espacio_obligado import EspacioObligado
from models.espacio_user import EspacioUser

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


@app.post("/register/")
def create_user(user_data: UserLogin, db: Session = Depends(get_db)):
    """Create a new user"""
    user, message = User.create(
        email=user_data.email, password=user_data.password, db=db
    )
    if not user:
        return HTTPException(status_code=400, detail=message)
    return {"success": True, "email": user.email, "id": user.id}


@app.post("/login/")
def login_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Login a user"""
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
    """Get current user"""
    return current_user


@app.get("/entidades/")
async def get_entidades():  # (current_user: dict = Depends(get_current_user)):
    """Get entidades con sedes y sus espacios obligados"""
    entidades_dict = Entidad.get_all(db=SessionLocal())
    return {"data": entidades_dict}


@app.get("/entidades/{entidad_id}/")
async def get_entidad(entidad_id: int, current_user: dict = Depends(get_current_user)):
    entidad = Entidad.get_by_id(entidad_id, db=SessionLocal())
    if not entidad:
        return HTTPException(status_code=400, detail="Entidad no encontrada")
    return {"data": entidad.to_dict_list()}


@app.get("/provincias/")
async def get_provincias(current_user: dict = Depends(get_current_user)):
    """Get provincias"""
    user_has_role(current_user, "representante")
    provincias = Provincia.get_all(db=SessionLocal())
    return {"data": provincias}


@app.post("/entidades/")
async def create_entidad(
    entidad: EntidadSchema, current_user: dict = Depends(get_current_user)
):
    """Create entidad"""
    user_has_role(current_user, "representante")
    entidad, message = Entidad.create(entidad, current_user["id"], db=SessionLocal())
    if not entidad:
        return HTTPException(status_code=400, detail=message)
    return {"success": True, "entidad": entidad.to_dict_list()}


@app.post("/sede/")
async def create_sede(
    sede_data: SedeSchema,
    current_user: dict = Depends(get_current_user),
):
    """Create sede"""
    user_has_role(current_user, "representante")
    entidad = Entidad.get_by_id(sede_data.entidad_id, db=SessionLocal())
    if not entidad:
        return HTTPException(status_code=400, detail="Entidad no encontrada")
    sede, message = Sede.create(sede_data, current_user["id"], db=SessionLocal())
    if not sede:
        return HTTPException(status_code=400, detail=message)
    return {"success": True, "sede": sede.to_dict_list()}


@app.post("/espacios_obligados/")
async def create_espacio_obligado(
    espacio_obligado: EspacioObligadoSchema,
    current_user: dict = Depends(get_current_user),
):
    """Create espacio obligado"""
    user_has_role(current_user, "representante")
    sede = Sede.get_by_id(espacio_obligado.sede_id, db=SessionLocal())
    if not sede:
        return HTTPException(status_code=400, detail="Sede no encontrada")
    _espacio_obligado, message = EspacioObligado.create(
        espacio_obligado, current_user["id"], db=SessionLocal()
    )
    if not _espacio_obligado:
        return HTTPException(status_code=400, detail=message)
    solicitud, message = EspacioUser.create(
        current_user["id"],
        _espacio_obligado.id,
        db=SessionLocal(),
        al_crear_espacio=True,
    )
    if not solicitud:
        return HTTPException(
            status_code=400, detail="Error al solicitar administracion"
        )

    return {"success": True, "espacio_obligado": espacio_obligado.to_dict_list()}


@app.post("/solicitar_administracion/{espacio_obligado_id}/")
async def solicitar_administracion(
    espacio_obligado_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Solicitar administracion de espacio obligado"""
    user_has_role(current_user, "representante")
    espacio_obligado = EspacioObligado.get_by_id(espacio_obligado_id, db=SessionLocal())
    if not espacio_obligado:
        return HTTPException(status_code=400, detail="Espacio obligado no encontrado")
    solicitud, message = EspacioUser.create(
        current_user["id"],
        espacio_obligado_id,
        db=SessionLocal(),
        al_crear_espacio=False,
    )
    if not solicitud:
        return HTTPException(status_code=400, detail=message)

    return {"success": True}


@app.get("/solicitudes_administracion/")
async def solicitudes_administracion(
    current_user: dict = Depends(get_current_user),
):
    """Solicitudes de administracion de espacio obligado"""
    user_has_role(current_user, "administrador_provincial")
    solicitudes = EspacioUser.get_pending(
        current_user["provincia_id"], db=SessionLocal()
    )
    return {"data": solicitudes}


@app.post("/aceptar_administracion/{espacio_obligado_id}/{user_id}/}")
async def aceptar_administracion(
    espacio_obligado_id: int,
    user_id: int,
    aprobar: bool,
    current_user: dict = Depends(get_current_user),
):
    """Aceptar administracion de espacio obligado"""
    user_has_role(current_user, "administrador_provincial")
    tiene_jurisdiccion, message = EspacioObligado.tiene_jurisdiccion(
        espacio_obligado_id, current_user["provincia_id"]
    )
    if not tiene_jurisdiccion:
        return HTTPException(status_code=400, detail=message)
    solicitud = EspacioUser.get_by_user_and_espacio(
        user_id, espacio_obligado_id, db=SessionLocal()
    )
    if not solicitud or not solicitud.pending:
        return HTTPException(status_code=400, detail="Solicitud no encontrada")
    solicitud.valida = aprobar
    solicitud.pending = False
    solicitud, message = EspacioUser.save(solicitud, db=SessionLocal())
    if not solicitud:
        return HTTPException(status_code=500, detail=message)
    return {"success": True}


# @app.post("/solicitar_administracion/{espacio_obligado_id}/")
# async def solicitar_administracion(

# @app.get("/sede/{sede_id}/")
# async def get_sede(sede_id: int, current_user: dict = Depends(get_current_user)):
#     """Get sede"""
#     user_has_role(current_user, "representante")
#     sede = Sede.get_by_id(sede_id, db=SessionLocal())
#     if not sede:
#         return HTTPException(status_code=400, detail="Sede no encontrada")

#     return {"success": True, "sede": sede.to_dict_list()}


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")
