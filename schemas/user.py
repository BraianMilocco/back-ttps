from pydantic import BaseModel


class UserBasic(BaseModel):
    email: str
    password: str


class UserCreate(UserBasic):
    pass


class UserLogin(UserBasic):
    pass
