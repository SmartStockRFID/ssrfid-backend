import datetime

from pydantic import BaseModel, ConfigDict

from app.models.conferencia import Conferencia


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
    ultima_leitura: datetime.datetime
    quantidade: int


class LeituraCreate(LeituraBase):
    lido_em: datetime.datetime
    rfid_etiqueta: str


class ConferenciaBase(BaseModel):
    username_funcionario: str


class ConferenciaOut(ConferenciaBase):
    id: int
    status: str
    leituras: list[LeituraOut]
    eventos: list[EventoOut]

    @classmethod
    def from_conferencia_model(cls, nova_conferencia: Conferencia):
        return cls(
            id=nova_conferencia.id,
            status=nova_conferencia.status,
            username_funcionario=nova_conferencia.funcionario.username,
            leituras=[
                LeituraOut(
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
