from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    username: str
    role: str

class UsuarioCreate(BaseModel):
    username: str
    password: str
    role: str

class UsuarioOut(UsuarioBase):
    id: int
    class Config:
        from_attributes = True
