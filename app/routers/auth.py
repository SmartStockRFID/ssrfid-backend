from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_user,
    verify_token,
)
from app.crud.usuario import get_usuario_by_username
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import (
    LoginResponse,
    RefreshTokenRequest,
    TokenResponse,
    UsuarioOut,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Realiza login de usuário no padrão Oauth2.
    Retorna access_token (validade: 1h) e refresh_token (validade: 7 dias).
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha inválidos")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")

    access_token, access_expire = create_access_token(data={"sub": user.username, "role": user.role})
    refresh_token, refresh_expire = create_refresh_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "access_expire": access_expire,
        "refresh_expire": refresh_expire,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Gera um novo access_token a partir de um refresh_token válido.

    Body:
    {
        "refresh_token": "seu_refresh_token_aqui"
    }
    """
    payload = verify_token(token_data.refresh_token, token_type="refresh")

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de refresh inválido ou expirado"
        )

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de refresh inválido")

    # Busca usuário no banco
    user = get_usuario_by_username(db, username)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário inativo")

    # Gera novo access token
    new_access_token, access_expire = create_access_token(data={"sub": user.username, "role": user.role})
    refresh_token, refresh_expire = create_refresh_token(data={"sub": user.username})

    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,
        "access_expire": access_expire,
        "refresh_expire": refresh_expire,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UsuarioOut)
def get_usuario_atual(current_user: Usuario = Depends(get_current_user)):
    """
    Obtém o usuário atualmente logado
    """
    return UsuarioOut(
        id=current_user.id,
        username=current_user.username,
        role=current_user.role,
    )
