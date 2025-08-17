from sqlalchemy.orm import Session

from app.crud.usuario import get_usuario_by_username
from app.models.conferencia import Conferencia, StatusConferencia
from app.schemas.conferencia import ConferenciaCreate, ConferenciaOut


def existe_conferencia_ativa(session: Session) -> bool:
    return session.query(Conferencia).filter(Conferencia.status == StatusConferencia.INICIADA).count() > 0


def criar_conferencia(session: Session, nova_conferencia: ConferenciaCreate) -> ConferenciaOut:
    funcionario_rel = get_usuario_by_username(session, nova_conferencia.username_funcionario)

    conferencia = Conferencia(
        **nova_conferencia.model_dump(exclude=["id", "username_funcionario"]),
        id_funcionario=funcionario_rel.id,
    )

    session.add(conferencia)
    session.commit()

    return ConferenciaOut(
        id=nova_conferencia.id,
        username_funcionario=funcionario_rel.username,
        eventos=nova_conferencia.eventos,
        leituras=nova_conferencia.leituras,
    )
