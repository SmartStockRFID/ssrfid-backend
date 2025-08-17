import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.peca import Peca  # noqa
from app.models.usuario import Usuario  # noqa


class StatusConferencia(str, enum.Enum):
    INICIADA = "iniciada"
    FINALIZADA = "finalizada"
    CANCELADA = "cancelada"


class Etiqueta(Base):
    __tablename__ = "etiqueta"

    id = Column(Integer, primary_key=True, index=True)
    rfid_uid = Column(String, unique=True, nullable=True)
    epc = Column(String, unique=True, nullable=True)
    peca_id = Column(Integer, ForeignKey("pecas.id"))


class Leitura(Base):
    __tablename__ = "leitura"
    id = Column(Integer, primary_key=True, index=True)
    etiqueta_id = Column(Integer, ForeignKey("etiqueta.id"))
    conferencia_id = Column(Integer, ForeignKey("conferencia.id"))
    timestamp_leitura = Column(DateTime(timezone=True), server_default=func.now())

    etiqueta = relationship("Etiqueta")
    conferencia = relationship("Conferencia", back_populates="leituras")


class Evento(Base):
    __tablename__ = "evento"
    id = Column(Integer, primary_key=True, index=True)
    tipo_evento = Column(String, nullable=False)
    ocorreu_em = Column(DateTime(timezone=True), nullable=False)
    conferencia_id = Column(Integer, ForeignKey("conferencia.id"))

    conferencia = relationship("Conferencia")


class Conferencia(Base):
    __tablename__ = "conferencia"
    id = Column(Integer, primary_key=True, index=True)
    id_funcionario = Column(Integer, ForeignKey("usuarios.id"))
    iniciada_em = Column(DateTime(timezone=True), server_default=func.now())
    finalizada_em = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(StatusConferencia), nullable=False, default=StatusConferencia.INICIADA)

    leituras = relationship("Leitura", back_populates="conferencia")
    eventos = relationship("Evento", back_populates="conferencia")
