from pydantic import BaseModel, validator
from datetime import datetime, timezone


class ReparacionDeaSchema(BaseModel):
    fecha_inicio: datetime
    fecha_fin: datetime
    tecnico: str

    @validator("fecha_inicio")
    def validate_fecha(cls, value):
        now = datetime.now(timezone.utc)
        if value > now:
            raise ValueError("La fecha no puede ser futura")
        return value

    @validator("fecha_fin")
    def validate_fecha(cls, value):
        now = datetime.now(timezone.utc)
        if value > now:
            raise ValueError("La fecha no puede ser futura")
        return value
