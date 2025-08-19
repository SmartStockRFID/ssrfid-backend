from sqlalchemy.orm import Session, joinedload

from app.crud.usuario import get_usuario_by_username
from app.models.conferencia import Conferencia, Etiqueta, Evento, Leitura, StatusConferencia
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


def registrar_leituras_em_conferencia(
    session: Session,
    conferencia_atual: Conferencia,
    leituras: list[LeituraCreate],
) -> Conferencia | None:
    leituras_registradas = []
    for leitura in leituras:
        etiqueta = (
            session.query(Etiqueta)
            .options(joinedload(Etiqueta.produto))
            .filter(Etiqueta.codigo_oem == leitura.codigo_oem)
            .one_or_none()
        )

        if not etiqueta:
            continue

        leituras_registradas.append(
            Leitura(
                etiqueta=etiqueta,
                conferencia=conferencia_atual,
                timestamp_leitura=leitura.lido_em,
            )
        )

    session.add_all(leituras_registradas)
    conferencia_atual.leituras.extend(leituras_registradas)
    session.commit()

    return conferencia_atual


def existe_conferencia_ativa(session: Session) -> bool:
    return session.query(Conferencia).filter(Conferencia.status == StatusConferencia.INICIADA).count() > 0


def get_conferencia_by_id(session: Session, conferencia_id: int) -> Conferencia:
    return (
        session.query(Conferencia)
        .options(joinedload(Conferencia.leituras))
        .filter(Conferencia.id == conferencia_id)
        .first()
    )


def get_conferencias(session: Session) -> list[Conferencia]:
    return session.query(Conferencia).all()


def criar_conferencia(session: Session, nova_conferencia: ConferenciaCreate) -> Conferencia:
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
