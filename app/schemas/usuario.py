import datetime
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


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    """Schema para resposta de login e refresh token."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    access_expire: datetime.datetime
    refresh_expire: datetime.datetime


class LoginResponse(TokenResponse):
    """Schema para resposta de login com refresh token."""

    refresh_token: str


class TokenVerifyResponse(BaseModel):
    """Schema para resposta de verificação de token."""

    valid: bool
    username: str
    role: RoleEnum
    is_active: bool
