from pydantic import BaseModel, validator
import re


class UserBasic(BaseModel):
    email: str
    password: str

    @validator("email")
    def email_must_be_valid(cls, value):
        pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        if not re.match(pattern, value):
            raise ValueError("email no es válido")

        return value


class UserCreate(UserBasic):
    pass


class UserLogin(UserBasic):
    pass
