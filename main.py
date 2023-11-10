from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    WebSocket,
    WebSocketDisconnect,
    BackgroundTasks,
)
from typing import Dict, List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from db.base import Base
from db.session import SessionLocal, engine
from settings import settings

# Helpers
from helpers import (
    create_access_token,
    get_data_from_token,
    get_dea_marcas,
    get_dea_modelos,
)

# Schemas
from schemas.user import UserCreate, UserLogin
from schemas.espacios_obligados import (
    EspacioObligado as EspacioObligadoSchema,
    Ddjj as DdjjSchema,
)
from schemas.entidad import Entidad as EntidadSchema
from schemas.sede import Sede as SedeSchema, SedeCompleta as SedeCompletaSchema
from schemas.responsables import ResponsablesSchema
from schemas.visita import Visita as VisitaSchema
from schemas.dea import DeaSchema
from schemas.reparacion_dea import ReparacionDeaSchema
from schemas.muerte_subita import MueteSubitaSchema
from schemas.inconvenientes import InconvenientesSchema
from schemas.solicitud_dea import SolicitudDeaSchema, SolicitudDeaCompletaSchema

# Models
from models.user import User
from models.entidad import Entidad
from models.provincia import Provincia
from models.sede import Sede
from models.espacio_obligado import EspacioObligado
from models.espacio_user import EspacioUser
from models.responsable_sede import ResponsableSede
from models.visita import Visita
from models.dea import Dea
from models.notificacion import Notificacion
from models.reparacion_dea import ReparacionDea
from models.muerte_subita import MuerteSubita
from models.incovenientes import Incovenientes
from models.solicitar_dea import SolicitudDea

from mail import render_email_template, send_email

# CREAR MODEL MANTEMIENTO fecha, dea
app = FastAPI()
# Configuración del middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tokenUrl = "/login/"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=tokenUrl)


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id in self.active_connections:
            self.active_connections[room_id].append(websocket)
        else:
            self.active_connections[room_id] = [websocket]

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)

    async def broadcast(self, room_id: str, message: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)

    async def close_room(self, room_id: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.close()
            del self.active_connections[room_id]


manager = ConnectionManager()


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
    print(user)
    if not user["rol"] == rol:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Permiso Denegado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


db = SessionLocal()


def get_db():
    return db


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
    entidades_dict = Entidad.get_all(db=get_db())
    return {"data": entidades_dict}


@app.get("/entidades/{entidad_id}/")
async def get_entidad(entidad_id: int, current_user: dict = Depends(get_current_user)):
    entidad = Entidad.get_by_id(entidad_id, db=get_db())
    if not entidad:
        return HTTPException(status_code=400, detail="Entidad no encontrada")
    return {"data": entidad.to_dict_list()}


@app.get("/provincias/")
async def get_provincias():
    """Get provincias"""
    provincias = Provincia.get_all(db=get_db())
    return {"data": provincias}


@app.post("/entidades/")
async def create_entidad(
    entidad: EntidadSchema, current_user: dict = Depends(get_current_user)
):
    """Create entidad"""
    user_has_role(current_user, "representante")
    entidad, message = Entidad.create(entidad, current_user["id"], db=get_db())
    if not entidad:
        return HTTPException(status_code=400, detail=message)
    return {"success": True, "data": entidad.to_dict_list()}


@app.post("/sedes/")
async def create_sede(
    sede_data: SedeSchema,
    current_user: dict = Depends(get_current_user),
):
    """Create sede"""
    user_has_role(current_user, "representante")
    entidad = Entidad.get_by_id(sede_data.entidad_id, db=get_db())
    if not entidad:
        return HTTPException(status_code=400, detail="Entidad no encontrada")
    sede, message = Sede.create(sede_data, current_user["id"], db=get_db())
    if not sede:
        return HTTPException(status_code=400, detail=message)
    return {"success": True, "data": sede.to_dict_list()}


@app.post("/sedes/{sede_id}/")
async def completar_sedes(
    sede_id: int,
    sede_data: SedeCompletaSchema,
    current_user: dict = Depends(get_current_user),
):
    """Completar todos los datos de la sede"""
    user_has_role(current_user, "representante")
    sede = Sede.get_by_id(sede_id, db=get_db())
    if not sede:
        raise HTTPException(status_code=400, detail="Sede no encontrada")
    user_is_admin = EspacioUser.user_is_admin_sede(current_user["id"], sede_id, db)
    if not user_is_admin:
        raise HTTPException(status_code=400, detail="No es administrador de la sede")
    sede, message = sede.update(sede_data, db=get_db())
    if not sede:
        raise HTTPException(status_code=500, detail=message)
    return {"success": user_is_admin}


@app.get("/sedes/{espacio_id}/")
async def get_sede_espacio(
    espacio_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Completar todos los datos de la sede"""
    user_has_role(current_user, "representante")
    espacio = EspacioObligado.get_by_id(espacio_id, db=get_db())
    if not espacio:
        raise HTTPException(status_code=400, detail="Espacio no encontrado")
    user_is_admin = EspacioUser.user_is_admin_espacio(
        current_user["id"], espacio_id, db
    )
    if not user_is_admin:
        raise HTTPException(status_code=400, detail="No es administrador del espacio")
    sede = espacio.sede.to_dict_list_sin_espacio()
    return {"data": sede}


@app.post("/espacios_obligados/")
async def create_espacio_obligado(
    espacio_obligado: EspacioObligadoSchema,
    current_user: dict = Depends(get_current_user),
):
    """Create espacio obligado"""
    user_has_role(current_user, "representante")
    sede = Sede.get_by_id(espacio_obligado.sede_id, db=get_db())
    if not sede:
        raise HTTPException(status_code=400, detail="Sede no encontrada")
    _espacio_obligado, message = EspacioObligado.create(
        espacio_obligado, current_user["id"], db=get_db()
    )
    if not _espacio_obligado:
        raise HTTPException(status_code=400, detail=message)

    return {"success": True, "data": _espacio_obligado.to_dict_list()}


@app.get("/espacios_obligados/")
async def get_espacio_obligado(
    sede: int = None,
    current_user: dict = Depends(get_current_user),
):
    """Get espacio obligado"""
    espacios = []
    if sede:
        espacio = EspacioObligado.get_by_sede_id(sede, db=get_db())
        espacios = espacio.to_dict_user_list(current_user["id"])
    else:
        user = User.get_by_email(current_user["email"], db=get_db())
        espacios = user.get_espacios()
    return {"data": espacios}


@app.get("/espacios_obligados/{espacio_id}/")
async def get_espacio_obligado(
    espacio_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Get espacio obligado"""
    espacio_obligado = EspacioObligado.get_by_id(espacio_id, db=get_db())
    if not espacio_obligado:
        raise HTTPException(status_code=400, detail="Espacio obligado no encontrado")
    return {"data": espacio_obligado.to_dict_user_list(current_user["id"])}


@app.post("/ddjj/{espacio_obligado_id}/")
async def cargar_ddjj(
    espacio_obligado_id: int,
    ddjj: DdjjSchema,
    current_user: dict = Depends(get_current_user),
):
    """Cargar ddjj y si corresponde cambia el estado del espacio obligado"""
    user_has_role(current_user, "representante")
    espacio_obligado = EspacioObligado.get_by_id(espacio_obligado_id, db=get_db())
    if not espacio_obligado:
        raise HTTPException(status_code=400, detail="Espacio obligado no encontrado")
    print(espacio_obligado)
    if not espacio_obligado.puede_completar_ddjj_dea:
        raise HTTPException(
            status_code=400, detail="La sede no tiene toda la informacion completa"
        )
    user_is_admin = EspacioUser.user_is_admin_espacio(
        current_user["id"], espacio_obligado_id, db
    )
    if not user_is_admin:
        raise HTTPException(status_code=400, detail="No es administrador del espacio")
    espacio_obligado, message = espacio_obligado.update_ddjj(ddjj, db=get_db())
    if not espacio_obligado:
        raise HTTPException(status_code=400, detail=message)
    return {"data": espacio_obligado.to_dict_list()}


@app.post("/deas/")
async def cargar_dea(
    dea_data: DeaSchema,
    current_user: dict = Depends(get_current_user),
):
    """Cargar dea. El modelo espera el nombre del dea"""
    user_has_role(current_user, "representante")
    espacio_obligado = EspacioObligado.get_by_id(
        dea_data.espacio_obligado_id, db=get_db()
    )
    if not espacio_obligado:
        raise HTTPException(status_code=400, detail="Espacio obligado no encontrado")
    if not espacio_obligado.puede_completar_ddjj_dea:
        raise HTTPException(
            status_code=400, detail="La sede no tiene toda la informacion completa"
        )
    user_is_admin = EspacioUser.user_is_admin_espacio(
        current_user["id"], dea_data.espacio_obligado_id, db
    )
    if not user_is_admin:
        raise HTTPException(status_code=400, detail="No es administrador del espacio")
    dea, message = Dea.create(dea_data, db=get_db())
    if not dea:
        raise HTTPException(status_code=400, detail=message)
    estado_actualizado, message = espacio_obligado.validar_ddjj(db=get_db())
    if not estado_actualizado:
        raise HTTPException(status_code=400, detail=message)
    return {"data": dea.to_dict_list()}


@app.get("/deas/{espacio_obligado_id}/")
async def get_deas(espacio_obligado_id: int):
    """Get deas de un espacio obligado"""
    espacio_obligado = EspacioObligado.get_by_id(espacio_obligado_id, db=get_db())
    if not espacio_obligado:
        raise HTTPException(status_code=400, detail="Espacio obligado no encontrado")
    deas = Dea.get_by_espacio_obligado(espacio_obligado_id, db=get_db())
    return {"data": deas}


@app.delete("/deas/{espacio_obligado_id}/{dea_id}/")
async def delete_dea(
    espacio_obligado_id: int,
    dea_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Delete dea"""
    user_has_role(current_user, "representante")
    user_is_admin = EspacioUser.user_is_admin_espacio(
        current_user["id"], espacio_obligado_id, db
    )
    espacio_obligado = EspacioObligado.get_by_id(espacio_obligado_id, db=get_db())
    if not espacio_obligado:
        raise HTTPException(status_code=400, detail="Espacio obligado no encontrado")
    if not user_is_admin:
        raise HTTPException(status_code=400, detail="No es administrador del espacio")
    dea = Dea.get_by_id(dea_id, db=get_db())
    if not dea:
        raise HTTPException(status_code=400, detail="Dea no encontrado")
    dea, message = Dea.delete(dea, db=get_db())
    if not dea:
        raise HTTPException(status_code=500, detail=message)
    estado_actualizado, message = espacio_obligado.validar_ddjj(db=get_db())
    if not estado_actualizado:
        raise HTTPException(status_code=500, detail=message)
    return {"success": True}


@app.post("/solicitar_administracion/{espacio_obligado_id}/")
async def solicitar_administracion(
    espacio_obligado_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Solicitar administracion de espacio obligado"""
    user_has_role(current_user, "representante")
    espacio_obligado = EspacioObligado.get_by_id(espacio_obligado_id, db=get_db())
    if not espacio_obligado:
        raise HTTPException(status_code=400, detail="Espacio obligado no encontrado")
    solicitud, message = EspacioUser.create(
        current_user["id"],
        espacio_obligado_id,
        db=get_db(),
        al_crear_espacio=False,
    )
    if not solicitud:
        raise HTTPException(status_code=400, detail=message)

    return {"success": True}


@app.get("/solicitudes_administracion/")
async def solicitudes_administracion(
    estado: str = "PENDIENTE",
    current_user: dict = Depends(get_current_user),
):
    """Solicitudes de administracion de espacio obligado"""
    user_has_role(current_user, "administrador_provincial")
    solicitudes = EspacioUser.get_pending(
        current_user["provincia_id"], estado, db=get_db()
    )
    return {"data": solicitudes}


@app.post("/aceptar_administracion/{espacio_obligado_id}/{user_id}/")
async def aceptar_administracion(
    espacio_obligado_id: int,
    user_id: int,
    aprobar: bool,
    current_user: dict = Depends(get_current_user),
):
    """Aceptar administracion de espacio obligado"""
    user_has_role(current_user, "administrador_provincial")
    tiene_jurisdiccion, message = EspacioObligado.tiene_jurisdiccion(
        espacio_obligado_id, current_user["provincia_id"], db=get_db()
    )
    if not tiene_jurisdiccion:
        raise HTTPException(status_code=400, detail=message)
    solicitud = EspacioUser.get_by_user_and_espacio(
        user_id, espacio_obligado_id, db=get_db()
    )
    if not solicitud or not solicitud.pendiente:
        raise HTTPException(status_code=400, detail="Solicitud no encontrada")
    solicitud.valida = aprobar
    solicitud.pendiente = False
    solicitud, message = solicitud.update(db=get_db())
    if not solicitud:
        raise HTTPException(status_code=500, detail=message)
    return {"success": True}


@app.get("/responsables/{sede_id}/")
async def get_responsables(
    sede_id: int, current_user: dict = Depends(get_current_user)
):
    """Retorna los responsables de una sede"""
    # user_has_role(current_user, "representante")
    sede = Sede.get_by_id(sede_id, db=get_db())
    if not sede:
        raise HTTPException(status_code=400, detail="Sede no encontrada")
    responsables = ResponsableSede.get_by_sede(sede_id, db)
    return {"data": responsables}


@app.post("/responsables/{sede_id}/")
async def crear_responsables(
    sede_id: int,
    data: ResponsablesSchema,
    current_user: dict = Depends(get_current_user),
):
    """Crea un responsable para una sede"""
    user_has_role(current_user, "representante")
    sede = Sede.get_by_id(sede_id, db=get_db())
    if not sede:
        raise HTTPException(status_code=400, detail="Sede no encontrada")
    user_is_admin = EspacioUser.user_is_admin_sede(current_user["id"], sede_id, db)
    if not user_is_admin:
        raise HTTPException(status_code=400, detail="No es administrador de la sede")
    responsable, message = ResponsableSede.create(data, sede_id, db)
    if not responsable:
        raise HTTPException(status_code=500, detail=message)
    return {"success": True}


@app.get("/resultados-posibles/visitas/")
def get_resultados_posibles():
    """Retorna los resultados posibles de una visita"""
    return {"data": ["Aprobado", "Rechazado", "Dado de baja"]}


@app.get("/visitas/")
async def get_visitas(
    current_user: dict = Depends(get_current_user),
):
    """Retorna las visitas de un espacio obligado"""
    user_has_role(current_user, "certificador")
    visitas = Visita.get_all(db=get_db())
    return {"data": visitas}


@app.get("/visitas/{espacio_obligado_id}/")
async def get_visitas_a_espacio(
    espacio_obligado_id: int,
    current_user: dict = Depends(get_current_user),
):
    """Retorna las visitas de un espacio obligado"""
    visitas = Visita.get_by_espacio_obligado(espacio_obligado_id, db=get_db())
    return {"data": visitas}


@app.post("/visitas/")
async def create_visita(
    visita_data: VisitaSchema,
    current_user: dict = Depends(get_current_user),
):
    """Crea una visita a un espacio obligado"""
    user_has_role(current_user, "certificador")
    espacio_obligado = EspacioObligado.get_by_id(
        visita_data.espacio_obligado, db=get_db()
    )
    if not espacio_obligado:
        raise HTTPException(status_code=400, detail="Espacio obligado no encontrado")
    tiene_jurisdiccion, message = EspacioObligado.tiene_jurisdiccion(
        visita_data.espacio_obligado, current_user["provincia_id"], db=get_db()
    )
    if not tiene_jurisdiccion:
        raise HTTPException(status_code=400, detail=message)
    visita, message = Visita.create(visita_data, current_user["id"], db=get_db())
    if not visita:
        raise HTTPException(status_code=500, detail=message)

    if visita.paso():
        espacio, message = espacio_obligado.certificar(db=get_db())
        if not espacio:
            raise HTTPException(status_code=500, detail=message)
    return {"data": visita.to_dict_list()}


@app.post("/activacion/dea/{dea_id}/")
async def activar_dea(
    dea_id: int, activo: bool, current_user: dict = Depends(get_current_user)
):
    """ "Activa o desactiva un dea"""
    user_has_role(current_user, "representante")
    dea = Dea.get_by_id(dea_id, db=get_db())
    if not dea:
        raise HTTPException(status_code=400, detail="Dea no encontrado")

    user_is_admin = EspacioUser.user_is_admin_espacio(
        current_user["id"], dea.espacio_obligado_id, db
    )
    if not user_is_admin:
        raise HTTPException(status_code=400, detail="No es administrador del espacio")
    dea, message = dea.update_activo(activo, db)
    if not dea:
        raise HTTPException(status_code=500, detail=message)
    return {"success": True}


@app.post("/reparacion/dea/{dea_id}/")
async def post_reparacion_dea(
    dea_id: int,
    data: ReparacionDeaSchema,
    current_user: dict = Depends(get_current_user),
):
    """Carga una reparacion a un dea"""
    user_has_role(current_user, "representante")
    dea = Dea.get_by_id(dea_id, db=get_db())
    if not dea:
        raise HTTPException(status_code=400, detail="Dea no encontrado")

    user_is_admin = EspacioUser.user_is_admin_espacio(
        current_user["id"], dea.espacio_obligado_id, db
    )
    if not user_is_admin:
        raise HTTPException(status_code=400, detail="No es administrador del espacio")
    reparacion_dea, message = ReparacionDea.create(data, dea_id, db)
    if not reparacion_dea:
        raise HTTPException(status_code=500, detail=message)
    return {"data": reparacion_dea.to_dict_list()}


@app.get("/reparacion/dea/{dea_id}/")
async def get_reparacion_dea(
    dea_id: int,
    current_user: dict = Depends(get_current_user),
):
    """muestra reparaciones a un dea"""
    user_has_role(current_user, "representante")
    dea = Dea.get_by_id(dea_id, db=get_db())
    if not dea:
        raise HTTPException(status_code=400, detail="Dea no encontrado")

    user_is_admin = EspacioUser.user_is_admin_espacio(
        current_user["id"], dea.espacio_obligado_id, db
    )
    if not user_is_admin:
        raise HTTPException(status_code=400, detail="No es administrador del espacio")

    reparaciones = ReparacionDea.get_by_dea_dict(dea_id, db)
    return {"data": reparaciones}


@app.post("/mantenimiento/dea/{dea_id}/")
async def mantenimiento_dea(
    dea_id: int, current_user: dict = Depends(get_current_user)
):
    """actualiza fecha de mantenimiento dea"""
    user_has_role(current_user, "representante")
    dea = Dea.get_by_id(dea_id, db=get_db())
    if not dea:
        raise HTTPException(status_code=400, detail="Dea no encontrado")

    user_is_admin = EspacioUser.user_is_admin_espacio(
        current_user["id"], dea.espacio_obligado_id, db
    )
    if not user_is_admin:
        raise HTTPException(status_code=400, detail="No es administrador del espacio")
    dea, message = dea.actualizar_fecha_ultimo_mantenimiento(db)
    if not dea:
        raise HTTPException(status_code=500, detail=message)
    return {"success": True}


@app.get("/notificaciones/")
async def get_notificaciones(current_user: dict = Depends(get_current_user)):
    """Retorna las notificaciones de un espacio obligado"""
    user_has_role(current_user, "representante")
    espacios_user = EspacioUser.get_espacios_id_user_administra(current_user["id"], db)
    notificaciones = Notificacion.notificaciones_de_los_ultimos_dias(espacios_user, db)
    return {"data": notificaciones}


@app.post("/admin/certificar/vencido/{espacio_obligado_id}/{key}/")
async def certificar_vencido(
    espacio_obligado_id: int,
    key: str,
):
    """Para uso de admin, se usa para poder certificar un espacio obligado con una fecha
    vencida, asi poder correr y mostrar el cron en tiempo real"""
    if key != settings.fake_cron_key:
        raise HTTPException(status_code=400, detail="Key invalida")
    espacio_obligado = EspacioObligado.get_by_id(espacio_obligado_id, db=get_db())
    if not espacio_obligado:
        raise HTTPException(status_code=400, detail="Espacio obligado no encontrado")
    espacio_obligado, message = espacio_obligado.certificar_vencido(db=get_db())
    if not espacio_obligado:
        raise HTTPException(status_code=500, detail=message)
    return {"success": True}


@app.post("/admin/vencer-certificado/{key}/")
async def vencer_certificado(key: str):
    """Para uso del Cron, se usa para cambiar los estados de todos los espacios obligados
    certificados con fecha vencida a vencidos"""
    if key != settings.fake_cron_key:
        raise HTTPException(status_code=400, detail="Key invalida")
    espacios_obligados = EspacioObligado.get_vencidos(db=get_db())
    for espacio_obligado in espacios_obligados:
        espacio_obligado.vencer_certificado(db=get_db())
    return {"success": True}


@app.get("/marcas/deas/")
async def get_deas_marcas(current_user: dict = Depends(get_current_user)):
    """Retorna los marcas de deas tomados de la api dada"""
    user_has_role(current_user, "representante")
    data = get_dea_marcas()
    if not data:
        raise HTTPException(status_code=500, detail="Error al obtener modelos")
    return {"data": data}


@app.get("/modelos/deas/{marca}/")
async def get_deas_modelos(marca: str, current_user: dict = Depends(get_current_user)):
    """Retorna los modelos validas para una marca especifica"""
    user_has_role(current_user, "representante")
    data = get_dea_modelos(marca)
    if not data:
        raise HTTPException(status_code=500, detail="Error al obtener modelos")
    return {"data": data}


@app.get("/muerte-subita/sexos/")
async def get_sexos_muerte_subita():
    """Returna los sexos posibles al cargar una muerte subita"""
    return ["Masculino", "Femenino", "X"]


@app.post("/muerte-subita/{espacio_obligado_id}/")
async def cargar_muerte_subita(
    espacio_obligado_id: int,
    data: MueteSubitaSchema,
    current_user: dict = Depends(get_current_user),
):
    """Crea una muerte subita"""
    user_has_role(current_user, "representante")
    user_is_admin = EspacioUser.user_is_admin_espacio(
        current_user["id"], espacio_obligado_id, db
    )
    if not user_is_admin:
        raise HTTPException(status_code=400, detail="No es administrador del espacio")
    muerte_subita, message = MuerteSubita.create(
        data, espacio_obligado_id, current_user["id"], db
    )
    if not muerte_subita:
        raise HTTPException(status_code=500, detail=message)
    return {"data": muerte_subita.to_dict_list()}


@app.get("/muerte-subita/{espacio_obligado_id}/")
async def get_muertes_subitas(
    espacio_obligado_id: int, current_user: dict = Depends(get_current_user)
):
    user_has_role(current_user, "representante")
    user_is_admin = EspacioUser.user_is_admin_espacio(
        current_user["id"], espacio_obligado_id, db
    )
    if not user_is_admin:
        raise HTTPException(status_code=400, detail="No es administrador del espacio")
    muertes_buitas = MuerteSubita.get_from_espacio(espacio_obligado_id, db)
    return {"data": muertes_buitas}


@app.post("/inconvenientes/{espacio_obligado_id}/{muerte_subita_id}/")
async def cargar_inconveniente(
    espacio_obligado_id: int,
    muerte_subita_id: int,
    data: InconvenientesSchema,
    current_user: dict = Depends(get_current_user),
):
    """Crea un inconveniente para una muerte subita"""
    user_has_role(current_user, "representante")
    user_is_admin = EspacioUser.user_is_admin_espacio(
        current_user["id"], espacio_obligado_id, db
    )
    if not user_is_admin:
        raise HTTPException(status_code=400, detail="No es administrador del espacio")
    muerte_subita = MuerteSubita.get_from_id_and_espacio(
        muerte_subita_id, espacio_obligado_id, db
    )
    if not muerte_subita:
        raise HTTPException(status_code=400, detail="Muerte subita no encontrada")
    inconveniente, message = Incovenientes.create(data, muerte_subita_id, db)
    if not inconveniente:
        raise HTTPException(status_code=500, detail=message)
    return {"data": inconveniente.to_dict_list()}


###### AHORA VIENEN ALGUNOS QUE PUEDEN SERVIR PARA LA APP DEL CIUDADANO


@app.get("/publico/deas/{provincia_id}/")
async def get_espacio_por_provincia(provincia_id: int):
    """Retorna los deas de una provincia"""
    sedes = Sede.get_by_provincia(provincia_id, db=get_db())
    data = []
    for sede in sedes:
        data += sede.list_deas()
    return {"data": data}


@app.get("/publico/espacios/{provincia_id}/")
async def get_espacio_por_provincia(
    provincia_id: int, lat: str = None, lon: str = None
):
    """Retorna los espacios obligados de una provincia junto con la data de sus deas"""
    sedes = Sede.get_by_provincia(provincia_id, db=get_db())
    data = []
    for sede in sedes:
        data += sede.list_espacios(lat, lon)

    data = sorted(data, key=lambda k: k["distancia"])
    return {"data": data}


@app.post("/publico/solicitar-dea/{espacio_obligado_id}/")
async def solicitar_dea(
    espacio_obligado_id, data: SolicitudDeaSchema, background_tasks: BackgroundTasks
):
    """Solicitar un dea"""
    espacio_obligado = EspacioObligado.get_by_id(espacio_obligado_id, db=get_db())
    if not espacio_obligado:
        raise HTTPException(status_code=400, detail="Espacio obligado no encontrado")
    solicitud, message = SolicitudDea.create(
        data,
        espacio_obligado_id,
        db=get_db(),
    )
    if not solicitud:
        raise HTTPException(status_code=400, detail=message)
    url_aviso = settings.front_url + f"/confirmar-solicitud/{solicitud.id}"
    url_maps = f"https://www.google.com/maps?q={data.latitud},{data.longitud}"
    html_content = render_email_template(
        data.latitud, data.longitud, url_aviso, url_maps
    )
    to = EspacioUser.get_emails_admins_espacio(espacio_obligado_id, db)
    await send_email(to, html_content)
    return {
        "success": True,
        "solictud": solicitud.to_dict_list(),
        "to": to,
    }


@app.get("/publico/solicitar-dea/{espacio_obligado_id}/")
async def get_solicitudes_dea(espacio_obligado_id: int):
    """Retorna las solicitudes de dea de un espacio obligado"""
    solicitudes = SolicitudDea.get_by_espacio_obligado(espacio_obligado_id, db=get_db())
    return {"data": solicitudes}


@app.put("/solicitar-dea/{solicitud_dea_id}/")
async def editar_solicitud_dea(
    solicitud_dea_id: int,
    data: SolicitudDeaCompletaSchema,
    current_user: dict = Depends(get_current_user),
):
    """Editar una solicitud de dea"""
    user_has_role(current_user, "representante")
    solicitud = SolicitudDea.get_by_id(solicitud_dea_id, db=get_db())
    if not solicitud:
        raise HTTPException(status_code=400, detail="Solicitud no encontrada")
    user_is_admin = EspacioUser.user_is_admin_espacio(
        current_user["id"], solicitud.espacio_obligado_id, db
    )
    if not user_is_admin:
        raise HTTPException(status_code=400, detail="No es administrador del espacio")
    solicitud, message = solicitud.update(data, db=get_db())
    if not solicitud:
        raise HTTPException(status_code=500, detail=message)
    return {"data": solicitud.to_dict_list()}


import requests
import urllib


@app.get("/publico/provincia/")
def get_pronvicia_id(lat: str, lon: str):
    API_BASE_URL = "https://apis.datos.gob.ar/georef/api/ubicacion"
    data = {"ubicaciones": [{"lat": lat, "lon": lon, "aplanar": True}]}
    results = requests.post(
        API_BASE_URL, json=data, headers={"Content-Type": "application/json"}
    ).json()
    parsed_results = [
        single_result["ubicacion"] if single_result["ubicacion"] else {}
        for single_result in results["resultados"]
    ]
    try:
        result = parsed_results[0]["provincia_nombre"]
    except Exception:
        result = "Buenos Aires"
    id_provincia = Provincia.get_id_from_nombre(result, db=get_db())
    return id_provincia


##################### WEB SOCKETS #####################
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = (
                await websocket.receive_text()
            )  # puedes manejar aquí los mensajes entrantes si es necesario
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)


@app.post("/dea-en-camino/{solicitud_dea_id}")
async def dea_on_the_way(solicitud_dea_id: int):
    """El endpoint solo le envia una notificacion a los usuarios conectados a la sala"""
    solicitud_id = str(solicitud_dea_id)
    solicitud = SolicitudDea.get_by_id(solicitud_dea_id, db=get_db())
    if not solicitud:
        raise HTTPException(status_code=400, detail="Solicitud no encontrada")
    solicitud.atendido(db=get_db())
    await manager.broadcast(solicitud_id, "Tu DEA está en camino!")


@app.post("/close-room/{room_id}")
async def close_room(room_id: str):
    if room_id in manager.active_connections:
        await manager.close_room(room_id)
        return {"message": "Room closed successfully"}
    else:
        raise HTTPException(status_code=404, detail="Room not found")


@app.get("/certificador/espacios-obligados/")
async def get_espacios_obligados(current_user: dict = Depends(get_current_user)):
    """Retorna los espacios obligados de un certificador"""
    user_has_role(current_user, "certificador")
    espacios = EspacioObligado.get_from_province(
        current_user["provincia_id"], db=get_db()
    )
    return {"data": espacios}


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")
