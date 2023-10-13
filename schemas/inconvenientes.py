from pydantic import BaseModel, validator
from datetime import datetime, timezone


class InconvenientesSchema(BaseModel):
    fecha: datetime
    falta_insumos: bool
    estaba_en_sitio: bool
    respondio_con_descargas_electricas: bool
    cantidad_de_descargas: int = 0
    extra_info: str = None

    @validator("fecha")
    def validate_fecha(cls, value):
        now = datetime.now(timezone.utc)
        if value > now:
            raise ValueError("La fecha no puede ser futura")
        return value

    @validator("cantidad_de_descargas")
    def validate_cantidad_de_descargas(cls, value):
        if value < 0:
            raise ValueError("La cantidad de descargas no puede ser negativa")
        return value
