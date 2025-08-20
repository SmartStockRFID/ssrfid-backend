from pydantic import BaseModel
from typing import Optional, List

class EtiquetaBase(BaseModel):
    codigo_oem: str
    rfid_uid: str
    peca_id: int

class EtiquetaCreate(EtiquetaBase):
    pass

class EtiquetaOut(EtiquetaBase):
    id: int
    class Config:
        orm_mode = True

class PecaBase(BaseModel):
    nome: str
    descricao: str
    localizacao: str
    quantidade: int
    preco_custo: float
    preco_venda: float
    modelo_carro: str
    ano_carro: str

class PecaCreate(PecaBase):
    pass

class PecaUpdate(PecaBase):
    pass

class PecaOut(PecaBase):
    id: int
    etiquetas: Optional[List[EtiquetaOut]] = []
    class Config:
        orm_mode = True
