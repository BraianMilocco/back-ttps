from pydantic import BaseModel


class Sede(BaseModel):
    nombre: str
    numero: int
    direccion: str
    latitud: str
    longitud: str
    provincia_id: int
    entidad_id: int
