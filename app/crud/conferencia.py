from typing import Tuple

from fastapi_filters import FilterValues
from fastapi_filters.ext.sqlalchemy import apply_filters
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import PecaNotFound
from app.crud.usuario import get_usuario_by_username
from app.models.conferencia import Conferencia, Evento, Leitura, StatusConferencia, TagLida
from app.models.peca import Peca
from app.schemas.conferencia import ConferenciaCreate, EventoCreate, LeituraCreate


def registrar_eventos_em_conferencia(
    session: Session,
    conferencia_atual: Conferencia,
    eventos: list[EventoCreate],
):
    eventos_criados = [
        Evento(
            **evento.model_dump(exclude=["tipo"]),
            tipo_evento=evento.tipo,
        )
        for evento in eventos
    ]
    session.add_all(eventos_criados)
    conferencia_atual.eventos.extend(eventos_criados)
    session.commit()

    return conferencia_atual


def limpar_tabela_tags(session: Session):
    session.execute(delete(TagLida))
    session.commit()


def pegar_tag_ou_criar(session: Session, conferencia_id: int, tag_rfid: str) -> Tuple[TagLida, bool]:
    stmt = (
        insert(TagLida)
        .values(conferencia_id=conferencia_id, rfid_uuid=tag_rfid)
        .on_conflict_do_nothing(index_elements=["rfid_uuid"])
        .returning(TagLida)
    )

    result = session.execute(stmt).fetchone()

    if result:
        instance = result[0]
        session.add(instance)
        return instance, True

    instance = session.query(TagLida).filter_by(conferencia_id=conferencia_id, rfid_uuid=tag_rfid).one()
    return instance, False


def registrar_leituras_em_conferencia(
    session: Session,
    conferencia_atual: Conferencia,
    leituras: list[LeituraCreate],
) -> Conferencia | None:
    for leitura in leituras:
        _, tag_foi_criada = pegar_tag_ou_criar(session, conferencia_atual.id, leitura.rfid_etiqueta)

        if not tag_foi_criada:
            continue  # TAG já lida, aborta

        produto = session.query(Peca).filter(Peca.codigo_produto == leitura.codigo_produto).one_or_none()
        if not produto:
            raise PecaNotFound(f"Produto {leitura.codigo_produto} não encontrado")

        stmt = (
            insert(Leitura)
            .values(
                conferencia_id=conferencia_atual.id,
                produto_id=produto.id,
                codigo_categoria=produto.codigo_produto,
                quantidade=1,
            )
            # Caso exista um conflito (leitura já registrada) atualiza somente a quantidade
            .on_conflict_do_update(
                index_elements=["conferencia_id", "produto_id"],
                set_={"quantidade": Leitura.quantidade + 1},
            )
        )

        session.execute(stmt)

    session.commit()
    return conferencia_atual


def existe_conferencia_ativa(session: Session) -> bool:
    return session.query(Conferencia).filter(Conferencia.status == StatusConferencia.INICIADA).count() > 0


def get_conferencia_ativa(session: Session) -> Conferencia | None:
    return session.query(Conferencia).filter(Conferencia.status == StatusConferencia.INICIADA).first()


def get_conferencia_by_id(session: Session, conferencia_id: int) -> Conferencia:
    return (
        session.query(Conferencia)
        .options(joinedload(Conferencia.leituras))
        .filter(Conferencia.id == conferencia_id)
        .first()
    )


def get_readings_from_conference(
    session: Session,
    *,
    filters: FilterValues,
    limit: int,
    offset: int,
    id_conference: int,
) -> list[Leitura]:
    if not session.query(Conferencia).filter(Conferencia.id == id_conference):
        return None
    stmt = select(Leitura).filter(Leitura.conferencia_id == id_conference).limit(limit).offset(offset)
    stmt_filtered = apply_filters(stmt, filters)
    result = session.execute(stmt_filtered)
    return result.scalars().all()


def get_events_from_conference(
    session: Session,
    *,
    filters: FilterValues,
    limit: int,
    offset: int,
    id_conference: int,
) -> list[Leitura]:
    if not session.query().filter(Conferencia.id == id_conference):
        return None
    stmt = select(Leitura).filter(Evento.conferencia_id == id_conference).limit(limit).offset(offset)
    stmt_filtered = apply_filters(stmt, filters)
    result = session.execute(stmt_filtered)
    return result.scalars().all()


def get_conferencias(session: Session) -> list[Conferencia]:
    return session.query(Conferencia).all()


def criar_conferencia(session: Session, nova_conferencia: ConferenciaCreate) -> Conferencia:
    limpar_tabela_tags(session)
    funcionario_rel = get_usuario_by_username(session, nova_conferencia.username_funcionario)
    conferencia = Conferencia(
        **nova_conferencia.model_dump(exclude=["id", "username_funcionario"]),
        id_funcionario=funcionario_rel.id,
    )
    session.add(conferencia)
    session.commit()
    return conferencia


def mudar_status_conferencia(
    session: Session,
    conferencia: Conferencia,
    status_conferencia: StatusConferencia,
) -> Conferencia:
    conferencia.status = status_conferencia
    session.add(conferencia)
    session.commit()
