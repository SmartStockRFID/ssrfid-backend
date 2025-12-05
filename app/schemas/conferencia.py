import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict

from app.models.conferencia import Conferencia


class PecaBase(BaseModel):
    nome: str
    codigo_produto: str
    descricao: str
    localizacao: str
    model_config = ConfigDict(from_attributes=True)


class ConferenciaStatus(Enum):
    INICIADA = "iniciada"
    FINALIZADA = "finalizada"
    CANCELADA = "cancelada"


class EventoBase(BaseModel):
    tipo: str
    descricao: str
    ocorreu_em: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class EventoOut(EventoBase):
    id: int


class EventoCreate(EventoBase):
    pass


class LeituraBase(BaseModel):
    codigo_produto: str
    model_config = ConfigDict(from_attributes=True)


class LeituraDetailsOut(LeituraBase):
    id: int
    produto: PecaBase
    ultima_leitura: datetime.datetime
    quantidade: int
    model_config = ConfigDict(from_attributes=True)


class LeituraMinimalOut(LeituraBase):
    id: int
    ultima_leitura: datetime.datetime
    quantidade: int
    model_config = ConfigDict(from_attributes=True)


class LeituraCreate(LeituraBase):
    lido_em: datetime.datetime
    rfid_etiqueta: str


class ConferenciaBase(BaseModel):
    username_funcionario: str


class ConferenciaDetailsOut(ConferenciaBase):
    id: int
    status: ConferenciaStatus
    leituras: list[LeituraMinimalOut]
    created_at: datetime.datetime
    eventos: list[EventoOut]

    @classmethod
    def from_conferencia_model(cls, nova_conferencia: Conferencia):
        return cls(
            id=nova_conferencia.id,
            status=nova_conferencia.status,
            created_at=nova_conferencia.created_at,
            username_funcionario=nova_conferencia.funcionario.username,
            leituras=[
                LeituraMinimalOut(
                    id=leitura.id,
                    codigo_produto=leitura.codigo_categoria,
                    ultima_leitura=leitura.ultima_leitura_em,
                    quantidade=leitura.quantidade or 0,
                )
                for leitura in nova_conferencia.leituras
            ],
            eventos=[
                EventoOut(
                    id=evento.id,
                    tipo=evento.tipo_evento,
                    descricao=evento.descricao,
                    ocorreu_em=evento.ocorreu_em,
                )
                for evento in nova_conferencia.eventos
            ],
        )


class ConferenciaCreate(ConferenciaBase):
    pass


class ConferenciaMinimalOut(ConferenciaBase):
    id: int
    created_at: datetime.datetime
    status: ConferenciaStatus

    @classmethod
    def from_conferencia_model(cls, nova_conferencia: Conferencia):
        return cls(
            id=nova_conferencia.id,
            created_at=nova_conferencia.created_at,
            status=nova_conferencia.status,
            username_funcionario=nova_conferencia.funcionario.username,
        )


class LeituraFilter:
    pass
