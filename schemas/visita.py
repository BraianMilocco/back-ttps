from pydantic import BaseModel, validator
from datetime import datetime, timezone


class Visita(BaseModel):
    fecha: datetime
    observaciones: str = None
    resultado: str
    espacio_obligado: int

    @validator("fecha")
    def validate_fecha(cls, value):
        now = datetime.now(timezone.utc)
        if value > now:
            raise ValueError("La fecha no puede ser futura")
        return value

    @validator("resultado")
    def validate_resultado(cls, value):
        RESULTADOS = ["Aprobado", "Rechazado", "Dado de baja"]
        if value not in RESULTADOS:
            raise ValueError("El resultado debe ser Aprobado, Rechazado o Dado de baja")
        return value

    @validator("espacio_obligado")
    def validate_espacio_obligado(cls, value):
        if value <= 0:
            raise ValueError("El id del espacio obligado debe ser mayor a cero")
        return value
