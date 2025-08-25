from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.exceptions import ConferenciaAlreadyClosed, ConferenciaNotFound, FuncionarioNotFound
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
    ConferenciaDetailsOut,
    ConferenciaMinimalOut,
    EventoCreate,
    LeituraCreate,
)

router = APIRouter(prefix="/conferencia", tags=["conferencia"])


@router.post("/", response_model=ConferenciaMinimalOut)
def iniciar_conferencia(nova_conferencia: ConferenciaCreate, db: Session = Depends(get_db)):
    """Inicia uma nova sessão de conferência de estoque."""
    if not get_usuario_by_username(db, nova_conferencia.username_funcionario):
        raise FuncionarioNotFound()
    if existe_conferencia_ativa(db):
        raise ConferenciaAlreadyClosed()
    conferencia_criada = criar_conferencia(db, nova_conferencia)
    return ConferenciaMinimalOut.from_conferencia_model(conferencia_criada)


@router.post("/{conferencia_id}/leitura", response_model=ConferenciaDetailsOut)
def registrar_leitura_na_conferencia(
    conferencia_id: int, leituras: list[LeituraCreate], db: Session = Depends(get_db)
):
    """Registra leituras de tags RFID em uma conferência ativa."""
    conferencia_found = get_conferencia_by_id(db, conferencia_id)
    if not conferencia_found:
        raise ConferenciaNotFound()
    if conferencia_found.status != StatusConferencia.INICIADA:
        raise ConferenciaAlreadyClosed()
    conferencia_atualizada = registrar_leituras_em_conferencia(db, conferencia_found, leituras)
    return ConferenciaDetailsOut.from_conferencia_model(conferencia_atualizada)


@router.post("/{conferencia_id}/evento", response_model=ConferenciaDetailsOut)
def registrar_eventos_na_conferencia(
    conferencia_id: int, eventos: list[EventoCreate], db: Session = Depends(get_db)
):
    """Registra eventos (ex: Pausa) em uma conferência ativa."""
    conferencia_found = get_conferencia_by_id(db, conferencia_id)
    if not conferencia_found:
        raise ConferenciaNotFound()
    if conferencia_found.status != StatusConferencia.INICIADA:
        raise ConferenciaAlreadyClosed()
    conferencia_atualizada = registrar_eventos_em_conferencia(db, conferencia_found, eventos)
    return ConferenciaDetailsOut.from_conferencia_model(conferencia_atualizada)


@router.put("/{conferencia_id}/encerrar", response_model=ConferenciaMinimalOut)
def encerrar_conferencia(conferencia_id: int, db: Session = Depends(get_db)):
    """Encerra uma conferência ativa, mudando seu status para 'FINALIZADA'."""
    conferencia_found = get_conferencia_by_id(db, conferencia_id)
    if not conferencia_found:
        raise ConferenciaNotFound()
    if conferencia_found.status != StatusConferencia.INICIADA:
        raise ConferenciaAlreadyClosed()
    mudar_status_conferencia(db, conferencia_found, StatusConferencia.FINALIZADA)
    return ConferenciaMinimalOut.from_conferencia_model(conferencia_found)


@router.put("/{conferencia_id}/cancelar", response_model=ConferenciaMinimalOut)
def cancelar_conferencia(conferencia_id: int, db: Session = Depends(get_db)):
    """Cancela uma conferência ativa, mudando seu status para 'CANCELADA'."""
    conferencia_found = get_conferencia_by_id(db, conferencia_id)
    if not conferencia_found:
        raise ConferenciaNotFound()
    if conferencia_found.status != StatusConferencia.INICIADA:
        raise ConferenciaAlreadyClosed()
    mudar_status_conferencia(db, conferencia_found, StatusConferencia.CANCELADA)
    return ConferenciaMinimalOut.from_conferencia_model(conferencia_found)


@router.get("/", response_model=list[ConferenciaMinimalOut])
def listar_conferencia(db: Session = Depends(get_db)):
    """Lista todas as conferências."""
    conferencias = get_conferencias(db)
    return [ConferenciaMinimalOut.from_conferencia_model(conferencia) for conferencia in conferencias]


@router.get("/{id_conferencia}", response_model=ConferenciaDetailsOut)
def detalhes_conferencia(id_conferencia: int, db: Session = Depends(get_db)):
    """Retorna os detalhes de uma conferência específica."""
    conferencia_found = get_conferencia_by_id(db, id_conferencia)
    if not conferencia_found:
        raise ConferenciaNotFound()
    return ConferenciaDetailsOut.from_conferencia_model(conferencia_found)
