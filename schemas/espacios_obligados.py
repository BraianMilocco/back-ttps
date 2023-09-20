from pydantic import BaseModel


class AprobarEspacioObligado(BaseModel):
    aprobado: bool
