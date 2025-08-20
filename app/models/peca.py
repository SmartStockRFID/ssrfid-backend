from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Peca(Base):
    __tablename__ = "pecas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    localizacao = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_custo = Column(Float, nullable=False)
    preco_venda = Column(Float, nullable=False)
    modelo_carro = Column(String, nullable=False)
    ano_carro = Column(String, nullable=False)
    codigo_tipo = Column(Integer)  # Referência à categoria

    etiquetas = relationship("Etiqueta", back_populates="peca", cascade="all, delete-orphan")


class Etiqueta(Base):
    __tablename__ = "etiquetas"

    id = Column(Integer, primary_key=True, index=True)
    codigo_oem = Column(String, unique=True, nullable=False)
    rfid_uid = Column(String, unique=True, nullable=False)
    peca_id = Column(Integer, ForeignKey("pecas.id"), nullable=False)

    peca = relationship("Peca", back_populates="etiquetas")
