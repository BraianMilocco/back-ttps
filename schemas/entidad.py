from pydantic import BaseModel


class Entidad(BaseModel):
    id: int
    cuit: str
    razon_social: str
