from pydantic import BaseModel, validator
from datetime import datetime, timezone


class MueteSubitaSchema(BaseModel):
    fecha: datetime
    sexo: str
    edad: int
    fallecio: bool
    rcp: bool
    tiempo_rcp: int = 0
    responsable_id: int

    @validator("fecha")
    def validate_fecha(cls, value):
        now = datetime.now(timezone.utc)
        if value > now:
            raise ValueError("La fecha no puede ser futura")
        return value

    @validator("sexo")
    def validate_sexo(cls, value):
        if value not in ["Masculino", "Femenino", "X"]:
            raise ValueError("El sexo no es válido")
        return value

    @validator("edad")
    def validate_edad(cls, value):
        if value < 0:
            raise ValueError("La edad no puede ser negativa")
        return value

    @validator("tiempo_rcp")
    def validate_tiempo_rcp(cls, value):
        if value < 0:
            raise ValueError("El tiempo de RCP no puede ser negativo")
        if not cls.rcp:
            raise ValueError(
                "No se puede establecer un tiempo de RCP si no se realizó RCP"
            )
        return value
