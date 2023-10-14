from pydantic import BaseModel, validator
from datetime import datetime, timezone
from typing import Optional


class SolicitudDeaSchema(BaseModel):
    latitud: str
    longitud: str


class SolicitudDeaCompletaSchema(BaseModel):
    atendido: bool = False
    fecha_atendido: Optional[datetime] = None
    dea_id: Optional[int] = None
    responsable_sede_id: Optional[int] = None

    @validator("fecha_atendido", pre=True, always=True)
    def validate_fecha_atendido(cls, value, values):
        now = datetime.now(timezone.utc)
        if not value:
            if "atendido" in values and values["atendido"]:
                raise ValueError("La fecha de atendido es obligatoria")
            return value
        value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        value = value.replace(tzinfo=timezone.utc)  # Definir la zona horaria como UTC
        if value and value > now:
            raise ValueError("La fecha no puede ser futura")
        if "atendido" in values and not values["atendido"]:
            return None
        return value

    @validator("dea_id", pre=True, always=True)
    def validate_dea_id(cls, value, values):
        if not value:
            return value
        if value < 0:
            raise ValueError("El id de la DEA no puede ser negativo")
        if "atendido" in values and not values["atendido"]:
            return None
        return value

    @validator("responsable_sede_id", pre=True, always=True)
    def validate_responsable_sede_id(cls, value, values):
        if not value:
            return value
        if value < 0:
            raise ValueError("El id del responsable de sede no puede ser negativo")
        if "atendido" in values and not values["atendido"]:
            return None
        return value
