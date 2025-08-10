from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Peca(Base):
    __tablename__ = "pecas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    codigo_oem = Column(String, unique=True, nullable=False)
    descricao = Column(String, nullable=False)
    localizacao = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_custo = Column(Float, nullable=False)
    preco_venda = Column(Float, nullable=False)
    modelo_carro = Column(String, nullable=False)
    ano_carro = Column(String, nullable=False)
    rfid_uid = Column(String, unique=True, nullable=True)
