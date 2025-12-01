import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.mixins import TimestampMixin
from app.models.peca import Peca  # noqa
from app.models.usuario import Usuario  # noqa


class StatusConferencia(str, enum.Enum):
    INICIADA = "iniciada"
    FINALIZADA = "finalizada"
    CANCELADA = "cancelada"


# Tabela somente para consultas otimizadas de unicidade
class TagLida(Base):
    __tablename__ = "tag_lida"
    id = Column(Integer, primary_key=True, index=True)
    conferencia_id = Column(Integer, ForeignKey("conferencia.id"), nullable=False)
    rfid_uuid = Column(String, nullable=False, unique=True)


class Leitura(Base):
    __tablename__ = "leitura"
    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("pecas.id"), nullable=False)
    conferencia_id = Column(Integer, ForeignKey("conferencia.id"), nullable=False)
    codigo_categoria = Column(String, nullable=False)
    quantidade = Column(Integer, default=0)
    ultima_leitura_em = Column(DateTime(timezone=True), server_default=func.now())

    produto = relationship("Peca")
    conferencia = relationship("Conferencia", back_populates="leituras")

    __table_args__ = (
        UniqueConstraint(
            "conferencia_id", "produto_id", name="uq_conferencia_produto"
        ),  # Garante que não exista o mesmo produto associado a mesma conferência, isso é controlado pela quantidade
    )


class Evento(Base):
    __tablename__ = "evento"
    id = Column(Integer, primary_key=True, index=True)
    tipo_evento = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    ocorreu_em = Column(DateTime(timezone=True), nullable=False)
    conferencia_id = Column(Integer, ForeignKey("conferencia.id"))

    conferencia = relationship("Conferencia")


class Conferencia(TimestampMixin, Base):
    __tablename__ = "conferencia"
    id = Column(Integer, primary_key=True, index=True)
    id_funcionario = Column(Integer, ForeignKey("usuarios.id"))
    iniciada_em = Column(DateTime(timezone=True), server_default=func.now())
    finalizada_em = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(StatusConferencia), nullable=False, default=StatusConferencia.INICIADA)

    funcionario = relationship("Usuario")
    leituras = relationship("Leitura", back_populates="conferencia")
    eventos = relationship("Evento", back_populates="conferencia")
