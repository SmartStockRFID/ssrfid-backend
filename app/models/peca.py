from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Peca(Base):
    __tablename__ = "pecas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    codigo_produto = Column(String, unique=True, nullable=False)
    descricao = Column(String, nullable=False)
    localizacao = Column(String, nullable=False)
