from pydantic import BaseModel


class EtiquetaBase(BaseModel):
    id_produto: int


class EtiquetaCreate(EtiquetaBase):
    codigo_oem: int
    rfid_etiqueta: int


class PecaBase(BaseModel):
    nome: str
    codigo_produto: str
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

    class Config:
        orm_mode = True
