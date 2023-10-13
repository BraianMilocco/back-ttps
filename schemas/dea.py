from pydantic import BaseModel, validator
from datetime import datetime, timezone
from helpers import get_dea_marcas, get_dea_modelos


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

    @validator("marca")
    def validate_marca(cls, value):
        if not value:
            raise ValueError("La Marca no puede ser vacía")
        deas = get_dea_marcas()
        if not deas:
            raise ValueError("No se pudo validar la marca de DEA")
        deas_names = [dea["marca"] for dea in deas]
        if value not in deas_names:
            raise ValueError("La Marca no es válido")
        return value

    @validator("modelo")
    def validate_modelo(cls, value):
        if not value:
            raise ValueError("El Modelo no puede ser vacío")
        modelos = get_dea_modelos(cls.marca)
        if not modelos:
            raise ValueError("No se pudo validar el modelo de DEA")
        modelos_names = [modelo["nombre"] for modelo in modelos]
        if value not in modelos_names:
            raise ValueError("El Modelo no es válido")
        return value
