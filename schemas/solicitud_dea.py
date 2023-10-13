from pydantic import BaseModel, validator
from datetime import datetime, timezone


class SolicitudDeaSchema(BaseModel):
    latitud: str
    longitud: str


class SolicitudDeaCompletaSchema(BaseModel):
    atendido: bool = False
    fecha_atendido: datetime = None
    dea_id: int
    responsable_sede_id: int

    @validator("fecha_atendido")
    def validate_fecha_atendido(cls, value):
        now = datetime.now(timezone.utc)
        if value > now:
            raise ValueError("La fecha no puede ser futura")
        if not cls.atendido:
            return None
        return value

    @validator("dea_id")
    def validate_dea_id(cls, value):
        if value < 0:
            raise ValueError("El id de la DEA no puede ser negativo")
        if not cls.atendido:
            return None
        return value

    @validator("responsable_sede_id")
    def validate_responsable_sede_id(cls, value):
        if value < 0:
            raise ValueError("El id del responsable de sede no puede ser negativo")
        if not cls.atendido:
            return None
        return value
