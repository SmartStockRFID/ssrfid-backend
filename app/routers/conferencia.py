from fastapi import APIRouter, Depends, Response, status
from fastapi_filters import FilterValues, create_filters_from_model
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ConferenciaAlreadyClosed,
    ConferenciaAlreadyOpened,
    ConferenciaNotFound,
    FuncionarioNotFound,
)
from app.crud.conferencia import (
    criar_conferencia,
    existe_conferencia_ativa,
    get_conferencia_ativa,
    get_conferencia_by_id,
    get_conferencias,
    get_events_from_conference,
    get_readings_from_conference,
    mudar_status_conferencia,
    registrar_eventos_em_conferencia,
    registrar_leituras_em_conferencia,
)
from app.crud.usuario import get_usuario_by_username
from app.database import get_db
from app.models.conferencia import StatusConferencia
from app.schemas.auth import CurrentUser
from app.schemas.conferencia import (
    ConferenciaCreate,
    ConferenciaDetailsOut,
    ConferenciaMinimalOut,
    EventoCreate,
    EventoOut,
    LeituraCreate,
    LeituraDetailsOut,
)
from app.schemas.shared import PaginatedResponse

router = APIRouter(prefix="/conferencia", tags=["conferencia"])


@router.post("", response_model=ConferenciaMinimalOut)
def iniciar_conferencia(nova_conferencia: ConferenciaCreate, user: CurrentUser, db: Session = Depends(get_db)):
    """Inicia uma nova sessão de conferência de estoque."""
    if not get_usuario_by_username(db, nova_conferencia.username_funcionario):
        raise FuncionarioNotFound()
    if existe_conferencia_ativa(db):
        raise ConferenciaAlreadyOpened()
    conferencia_criada = criar_conferencia(db, nova_conferencia)
    return ConferenciaMinimalOut.from_conferencia_model(conferencia_criada)


@router.post("/{conferencia_id}/leitura", response_model=ConferenciaMinimalOut)
def registrar_leitura_na_conferencia(
    conferencia_id: int, leituras: list[LeituraCreate], user: CurrentUser, db: Session = Depends(get_db)
):
    """Registra leituras de tags RFID em uma conferência ativa."""
    conferencia_found = get_conferencia_by_id(db, conferencia_id)
    if not conferencia_found:
        raise ConferenciaNotFound()
    if conferencia_found.status != StatusConferencia.INICIADA:
        raise ConferenciaAlreadyClosed()
    conferencia_atualizada = registrar_leituras_em_conferencia(db, conferencia_found, leituras)
    return ConferenciaMinimalOut.from_conferencia_model(conferencia_atualizada)


@router.post("/{conferencia_id}/evento", response_model=ConferenciaMinimalOut)
def registrar_eventos_na_conferencia(
    conferencia_id: int, eventos: list[EventoCreate], user: CurrentUser, db: Session = Depends(get_db)
):
    """Registra eventos (ex: Pausa) em uma conferência ativa."""
    conferencia_found = get_conferencia_by_id(db, conferencia_id)
    if not conferencia_found:
        raise ConferenciaNotFound()
    if conferencia_found.status != StatusConferencia.INICIADA:
        raise ConferenciaAlreadyClosed()
    conferencia_atualizada = registrar_eventos_em_conferencia(db, conferencia_found, eventos)
    return ConferenciaMinimalOut.from_conferencia_model(conferencia_atualizada)


@router.put("/{conferencia_id}/encerrar", response_model=ConferenciaMinimalOut)
def encerrar_conferencia(conferencia_id: int, user: CurrentUser, db: Session = Depends(get_db)):
    """Encerra uma conferência ativa, mudando seu status para 'FINALIZADA'."""
    conferencia_found = get_conferencia_by_id(db, conferencia_id)
    if not conferencia_found:
        raise ConferenciaNotFound()
    if conferencia_found.status != StatusConferencia.INICIADA:
        raise ConferenciaAlreadyClosed()
    mudar_status_conferencia(db, conferencia_found, StatusConferencia.FINALIZADA)
    return ConferenciaMinimalOut.from_conferencia_model(conferencia_found)


@router.put("/{conferencia_id}/cancelar", response_model=ConferenciaMinimalOut)
def cancelar_conferencia(conferencia_id: int, user: CurrentUser, db: Session = Depends(get_db)):
    """Cancela uma conferência ativa, mudando seu status para 'CANCELADA'."""
    conferencia_found = get_conferencia_by_id(db, conferencia_id)
    if not conferencia_found:
        raise ConferenciaNotFound()
    if conferencia_found.status != StatusConferencia.INICIADA:
        raise ConferenciaAlreadyClosed()
    mudar_status_conferencia(db, conferencia_found, StatusConferencia.CANCELADA)
    return ConferenciaMinimalOut.from_conferencia_model(conferencia_found)


@router.get("", response_model=list[ConferenciaMinimalOut])
def listar_conferencia(user: CurrentUser, db: Session = Depends(get_db)):
    """Lista todas as conferências."""
    conferencias = get_conferencias(db)
    return [ConferenciaMinimalOut.from_conferencia_model(conferencia) for conferencia in conferencias]


@router.get("/{id_conferencia}/leituras", response_model=PaginatedResponse[LeituraDetailsOut])
def readings_from_conference(
    id_conferencia: int,
    user: CurrentUser,
    limit: int,
    offset: int,
    db: Session = Depends(get_db),
    filters: FilterValues = Depends(
        create_filters_from_model(LeituraDetailsOut, exclude=["quantidade", "produto"])
    ),
):
    """Lista todas as leituras assossiadas a uma conferência"""
    conferencia_found = get_conferencia_by_id(db, id_conferencia)
    if not conferencia_found:
        raise ConferenciaNotFound
    readings = get_readings_from_conference(
        session=db, filters=filters, limit=limit, offset=offset, id_conference=id_conferencia
    )

    return PaginatedResponse(
        count=len(readings),
        items=[
            LeituraDetailsOut(
                id=reading.id,
                codigo_produto=reading.produto.codigo_produto,
                produto=reading.produto,
                quantidade=reading.quantidade,
                ultima_leitura=reading.ultima_leitura_em,
            )
            for reading in readings
        ],
        skip=offset,
        limit=limit,
    )


@router.get("/{id_conferencia}/eventos", response_model=PaginatedResponse[EventoOut])
def events_from_conference(
    id_conferencia: int,
    user: CurrentUser,
    limit: int,
    offset: int,
    db: Session = Depends(get_db),
    filters: FilterValues = Depends(create_filters_from_model(EventoOut)),
):
    conferencia_found = get_conferencia_by_id(db, id_conferencia)
    if not conferencia_found:
        raise ConferenciaNotFound
    events = get_events_from_conference(
        db,
        filters=filters,
        limit=limit,
        offset=offset,
        id_conference=id_conferencia,
    )
    return PaginatedResponse(
        count=len(events),
        items=[EventoOut(event) for event in events],
        skip=offset,
        limit=limit,
    )


@router.get("-ativa", response_model=ConferenciaDetailsOut)
def pegar_conferencia_ativa(user: CurrentUser, db: Session = Depends(get_db)):
    """Retorna a conferência ativa atualmente"""
    conferencia = get_conferencia_ativa(db)
    if not conferencia:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return ConferenciaDetailsOut.from_conferencia_model(conferencia)
