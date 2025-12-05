from typing import Generic, TypeVar

from pydantic import Field
from pydantic.generics import GenericModel

M = TypeVar("M")


class PaginatedResponse(GenericModel, Generic[M]):
    count: int = Field(description="Número de itens retornados na resposta")
    skip: int = Field(description="Offset de itens")
    limit: int = Field(description="Quantidade limite de itens por página")
    items: list[M] = Field(description="Lista de itens retornados")
