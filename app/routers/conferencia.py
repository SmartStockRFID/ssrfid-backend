from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.conferencia import criar_conferencia, existe_conferencia_ativa
from app.crud.usuario import get_usuario_by_id, get_usuario_by_username
from app.database import get_db
from app.schemas.conferencia import ConferenciaCreate, ConferenciaOut

router = APIRouter(prefix="/conferencia")


@router.post("/", response_model=ConferenciaOut)
def iniciar_conferencia(nova_conferencia: ConferenciaCreate, db: Session = Depends(get_db)):
    if not get_usuario_by_username(db, nova_conferencia.username_funcionario):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Funcionário especificado não existe")
    if existe_conferencia_ativa(db):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Existe uma conferência já ativa")
    conferencia_criada = criar_conferencia(db, nova_conferencia)
    return conferencia_criada


@router.post("/", response_model=ConferenciaOut)
def listar_conferencia(nova_conferencia: ConferenciaCreate, db: Session = Depends(get_db)):
    if not get_usuario_by_username(db, nova_conferencia.username_funcionario):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Funcionário especificado não existe")
    if existe_conferencia_ativa(db):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Existe uma conferência já ativa")
    conferencia_criada = criar_conferencia(db, nova_conferencia)
    return conferencia_criada
