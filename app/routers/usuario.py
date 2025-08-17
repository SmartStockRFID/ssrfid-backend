from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_admin
from app.crud.usuario import create_usuario, get_usuario_by_username
from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioOut

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("/", response_model=UsuarioOut, status_code=201)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if get_usuario_by_username(db, usuario.username):
        raise HTTPException(status_code=400, detail="Usuário já existe")
    return create_usuario(db, usuario)
