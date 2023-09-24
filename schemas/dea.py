from pydantic import BaseModel, validator
from datetime import datetime, timezone


class DeaSchema(BaseModel):
    numero_serie: str
    nombre: str
    marca: str
    modelo: str
    solidario: bool
    activo: bool
    fecha_ultimo_mantenimiento: datetime = None
    espacio_obligado_id: int

    @validator("fecha_ultimo_mantenimiento")
    def validate_fecha(cls, value):
        if not value:
            return value
        now = datetime.now(timezone.utc)
        if value > now:
            raise ValueError("La fecha no puede ser futura")
        return value
