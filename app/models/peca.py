
from sqlalchemy import Column, Integer, String

from app.models.base import Base


"""
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base
"""



class Peca(Base):
    __tablename__ = "pecas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    codigo_produto = Column(String, unique=True, nullable=False)
    descricao = Column(String, nullable=False)
    localizacao = Column(String, nullable=False)

"""
    quantidade = Column(Integer, nullable=False)
    preco_custo = Column(Float, nullable=False)
    preco_venda = Column(Float, nullable=False)
    modelo_carro = Column(String, nullable=False)
    ano_carro = Column(String, nullable=False)
    codigo_tipo = Column(Integer)  # Referência à categoria

"""