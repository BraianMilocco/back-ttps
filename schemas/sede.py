from pydantic import BaseModel, validator


class Sede(BaseModel):
    nombre: str
    numero: int
    direccion: str
    provincia_id: int
    entidad_id: int

    @validator("numero", "entidad_id")
    def validate_positive(cls, value):
        if value <= 0:
            raise ValueError("debe ser un número positivo")
        return value

    @validator("provincia_id")
    def validate_provincia_id(cls, value):
        if value < 0 or value > 23:
            raise ValueError("debe ser un número entre 0 y 23")
        return value


class SedeCompleta(BaseModel):
    sector: str
    tipo: str
    superficie: int
    latitud: str
    longitud: str
    cantidad_pisos: int
    cantidad_personas_externas: int
    cantidad_personas_estables: int

    @validator(
        "superficie",
        "cantidad_pisos",
        "cantidad_personas_externas",
        "cantidad_personas_estables",
    )
    def validate_positive(cls, value):
        if value <= 0:
            raise ValueError("debe ser un número positivo")
        return value

    @validator("sector", "tipo")
    def validate_sector(cls, value):
        SECTORES = ["publico", "privado"]
        if value not in SECTORES:
            raise ValueError(f"debe ser uno de {SECTORES}")
        return value
