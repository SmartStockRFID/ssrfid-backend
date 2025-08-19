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
    produto_id = Column(Integer, ForeignKey("pecas.id"), nullable=False)
    rdid_uuid = Column(String, nullable=False)
    codigo_oem = Column(String, nullable=False)

    produto = relationship("Peca")


class Leitura(Base):
    __tablename__ = "leitura"
    id = Column(Integer, primary_key=True, index=True)
    etiqueta_id = Column(Integer, ForeignKey("etiqueta.id"), nullable=False)
    conferencia_id = Column(Integer, ForeignKey("conferencia.id"), nullable=False)
    timestamp_leitura = Column(DateTime(timezone=True), server_default=func.now())

    etiqueta = relationship("Etiqueta")
    conferencia = relationship("Conferencia", back_populates="leituras")


class Evento(Base):
    __tablename__ = "evento"
    id = Column(Integer, primary_key=True, index=True)
    tipo_evento = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
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

    funcionario = relationship("Usuario")
    leituras = relationship("Leitura", back_populates="conferencia")
    eventos = relationship("Evento", back_populates="conferencia")
