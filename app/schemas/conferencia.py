import datetime

from pydantic import BaseModel


class EventoBase(BaseModel):
    tipo: str
    ocorreu_em: datetime.datetime


class LeituraBase(BaseModel):
    etiqueta_id: int
    produto_id: int
    lido_em: datetime.datetime


class LeituraOut(LeituraBase):
    id: int


class EventoOut(EventoBase):
    id: int


class ConferenciaBase(BaseModel):
    username_funcionario: str


class ConferenciaOut(ConferenciaBase):
    id: int
    leituras: list[LeituraOut]
    eventos: list[EventoOut]


class ConferenciaCreate(ConferenciaBase):
    pass
