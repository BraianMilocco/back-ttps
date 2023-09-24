from pydantic import BaseModel, validator


class EspacioObligado(BaseModel):
    nombre: str
    sede_id: int

    @validator("sede_id")
    def sede_id_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("sede_id debe ser un número positivo")
        return value


class AprobarEspacioObligado(BaseModel):
    aprobado: bool
