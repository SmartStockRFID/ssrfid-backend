from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.conferencia import (
    criar_conferencia,
    existe_conferencia_ativa,
    get_conferencia_by_id,
    get_conferencias,
    mudar_status_conferencia,
    registrar_eventos_em_conferencia,
    registrar_leituras_em_conferencia,
)
from app.crud.usuario import get_usuario_by_username
from app.database import get_db
from app.models.conferencia import StatusConferencia
from app.schemas.conferencia import (
    ConferenciaCreate,
    ConferenciaOut,
    EventoCreate,
    LeituraCreate,
)

router = APIRouter(prefix="/conferencia", tags=["conferencia"])


@router.post("/", response_model=ConferenciaOut)
def iniciar_conferencia(nova_conferencia: ConferenciaCreate, db: Session = Depends(get_db)):
    if not get_usuario_by_username(db, nova_conferencia.username_funcionario):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Funcionário especificado não existe")
    if existe_conferencia_ativa(db):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Existe uma conferência já ativa")
    conferencia_criada = criar_conferencia(db, nova_conferencia)
    return ConferenciaOut.from_conferencia_model(conferencia_criada)


@router.post("/{conferencia_id}/leitura", response_model=ConferenciaOut)
def registrar_leitura_na_conferencia(
    conferencia_id: int, leituras: list[LeituraCreate], db: Session = Depends(get_db)
):
    conferencia_found = get_conferencia_by_id(db, conferencia_id)
    if not conferencia_found:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Conferência com o id {conferencia_id} não existe")
    if conferencia_found.status != StatusConferencia.INICIADA:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Conferência com status inválido")
    conferencia_atualizada = registrar_leituras_em_conferencia(db, conferencia_found, leituras)
    return ConferenciaOut.from_conferencia_model(conferencia_atualizada)


@router.post("/{conferencia_id}/evento", response_model=ConferenciaOut)
def registrar_eventos_na_conferencia(
    conferencia_id: int, eventos: list[EventoCreate], db: Session = Depends(get_db)
):
    conferencia_found = get_conferencia_by_id(db, conferencia_id)
    if not conferencia_found:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Conferência com o id {conferencia_id} não existe")
    if conferencia_found.status != StatusConferencia.INICIADA:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Conferência com status inválido")
    conferencia_atualizada = registrar_eventos_em_conferencia(db, conferencia_found, eventos)
    return ConferenciaOut.from_conferencia_model(conferencia_atualizada)


@router.put("/{conferencia_id}/encerrar", response_model=ConferenciaOut)
def encerrar_conferencia(conferencia_id: int, db: Session = Depends(get_db)):
    conferencia_found = get_conferencia_by_id(db, conferencia_id)
    if not conferencia_found:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Conferência com o id {conferencia_id} não existe")
    if conferencia_found.status != StatusConferencia.INICIADA:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Conferência com status inválido")
    mudar_status_conferencia(db, conferencia_found, StatusConferencia.FINALIZADA)
    return ConferenciaOut.from_conferencia_model(conferencia_found)


@router.put("/{conferencia_id}/cancelar", response_model=ConferenciaOut)
def cancelar_conferencia(conferencia_id: int, db: Session = Depends(get_db)):
    conferencia_found = get_conferencia_by_id(db, conferencia_id)
    if not conferencia_found:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Conferência com o id {conferencia_id} não existe")
    if conferencia_found.status != StatusConferencia.INICIADA:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Conferência com status inválido")
    mudar_status_conferencia(db, conferencia_found, StatusConferencia.CANCELADA)
    return ConferenciaOut.from_conferencia_model(conferencia_found)


@router.get("/", response_model=list[ConferenciaOut])
def listar_conferencia(db: Session = Depends(get_db)):
    conferencias = get_conferencias(db)
    return [ConferenciaOut.from_conferencia_model(conferencia) for conferencia in conferencias]
