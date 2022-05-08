from datetime import datetime

from pydantic import BaseModel

from services.enums import RolesEnum


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    password: str
    role: RolesEnum
    date_joined: datetime
    active: bool

    class Config:
        orm_mode = True


class UserCreateUpdateSchema(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str

    
class UserLoginSchema(BaseModel):
    email: str
    password: str
