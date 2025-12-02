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


class LeituraOut(LeituraBase):
    id: int
    produto: PecaBase
    ultima_leitura: datetime.datetime
    quantidade: int
    model_config = ConfigDict(from_attributes=True)


class LeituraCreate(LeituraBase):
    lido_em: datetime.datetime
    rfid_etiqueta: str


class ConferenciaBase(BaseModel):
    username_funcionario: str


class ConferenciaCreate(ConferenciaBase):
    pass


class ConferenciaMinimalOut(ConferenciaBase):
    id: int
    status: ConferenciaStatus

    @classmethod
    def from_conferencia_model(cls, nova_conferencia: Conferencia):
        return cls(
            id=nova_conferencia.id,
            status=nova_conferencia.status,
            username_funcionario=nova_conferencia.funcionario.username,
        )


class LeituraFilter:
    pass
