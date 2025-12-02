from datetime import datetime, timedelta, timezone

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.exceptions import CredentialsException, UnauthorizedUser
from app.crud.usuario import get_usuario_by_username, verify_password
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import RoleEnum
from app.settings import app_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def authenticate_user(db: Session, username: str, password: str):
    user = get_usuario_by_username(db, username)

    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(
            minutes=app_settings.JWT_ACCESS_EXIPIRE_MINUTES,
        )
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, app_settings.JWT_SECRET, algorithm=app_settings.JWT_ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, app_settings.JWT_SECRET, algorithms=[app_settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException()
    except JWTError:
        raise CredentialsException()
    user = get_usuario_by_username(db, username)
    if user is None:
        raise CredentialsException()
    return user


def get_current_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    if not current_user or not current_user.is_active:
        raise CredentialsException()
    return current_user


def get_admin_user(current_user: Usuario = Depends(get_current_user)):
    if current_user.role != RoleEnum.admin:
        raise UnauthorizedUser()
    return current_user
