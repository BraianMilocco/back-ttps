from pydantic import BaseModel


class Entidad(BaseModel):
    cuit: str
    razon_social: str
