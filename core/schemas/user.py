from enum import Enum

from pydantic import BaseModel


class RolesEnum(Enum):
    ADMIN = 'admin'
    USER = 'user'


class User(BaseModel):
    name: str
    email: str
    role: RolesEnum