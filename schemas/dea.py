from pydantic import BaseModel, validator
from datetime import datetime, timezone
from helpers import get_dea_models


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

    @validator("modelo")
    def validate_modelo(cls, value):
        if not value:
            raise ValueError("El modelo no puede ser vacío")
        deas = get_dea_models()
        if not deas:
            raise ValueError("No se pudo validar el modelo de DEA")
        deas_names = [dea["modelo"] for dea in deas]
        if value not in deas_names:
            raise ValueError("El modelo no es válido")
        return value
