from pydantic import BaseModel
from typing import Optional

class PecaBase(BaseModel):
    nome: str
    codigo_oem: str
    descricao: str
    localizacao: str
    quantidade: int
    preco_custo: float
    preco_venda: float
    modelo_carro: str
    ano_carro: str
    rfid_uid: Optional[str] = None

class PecaCreate(PecaBase):
    pass

class PecaUpdate(PecaBase):
    pass

class PecaOut(PecaBase):
    id: int

    class Config:
        orm_mode = True
