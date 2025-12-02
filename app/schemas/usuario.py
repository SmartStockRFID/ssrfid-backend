from enum import StrEnum

from pydantic import BaseModel


class RoleEnum(StrEnum):
    admin: str = "admin"
    stockist: str = "stockist"


class UsuarioBase(BaseModel):
    username: str
    role: RoleEnum


class UsuarioCreate(BaseModel):
    username: str
    password: str
    role: RoleEnum


class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
