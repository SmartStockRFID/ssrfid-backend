from pydantic import BaseModel


class PecaBase(BaseModel):
    nome: str
    codigo_produto: str
    descricao: str
    localizacao: str


class PecaFilter(BaseModel):
    nome: str | None = None
    codigo_categoria: str | None = None


class PecaCreate(PecaBase):
    pass


class PecaUpdate(PecaBase):
    pass


class PecaOut(PecaBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
