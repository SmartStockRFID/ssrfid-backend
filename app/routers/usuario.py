from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_admin_user
from app.core.exceptions import UserAlreadyRegistered, UserNotFound
from app.crud.usuario import create_usuario, get_usuario_by_username, get_usuarios, inativar_usuario
from app.database import get_db
from app.schemas.auth import AdminUser
from app.schemas.usuario import UsuarioCreate, UsuarioOut

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
    dependencies=[Depends(get_admin_user)],
)


@router.post("", response_model=UsuarioOut, status_code=201)
def criar_usuario(
    usuario: UsuarioCreate,
    user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Criação de usuários
    """
    if get_usuario_by_username(db, usuario.username):
        raise UserAlreadyRegistered()
    return create_usuario(db, usuario)


@router.get("", response_model=list[UsuarioOut])
def listar_usuarios(
    user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Lista usuários cadastrados na aplicação
    """
    return get_usuarios(db)


@router.put("/{usuario_id}/inativar", response_model=UsuarioOut)
def inativar_usuario_route(
    usuario_id: int,
    user: AdminUser,
    db: Session = Depends(get_db),
):
    """
    Inativa um usuário dado seu ID
    """
    usuario = inativar_usuario(db, usuario_id)
    if not usuario:
        raise UserNotFound()
    if not usuario.is_active:
        return usuario
    return usuario
