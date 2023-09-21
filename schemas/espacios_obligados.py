from pydantic import BaseModel


class EspacioObligado(BaseModel):
    nombre: str
    sede_id: int


class AprobarEspacioObligado(BaseModel):
    aprobado: bool
