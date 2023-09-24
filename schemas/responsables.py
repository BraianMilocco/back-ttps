import re
from pydantic import BaseModel, validator


class ResponsablesSchema(BaseModel):
    nombre: str
    telefono: str
    email: str

    @validator("telefono")
    def telefono_must_be_int(cls, value):
        if not value.isdigit():
            raise ValueError("telefono debe ser un número")

        return value

    @validator("email")
    def email_must_be_valid(cls, value):
        pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        if not re.match(pattern, value):
            raise ValueError("email no es válido")

        return value
