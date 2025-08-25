from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logger import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de contexto assíncrono para a duração da aplicação.

    - Antes do yield: executa ações de inicialização (startup).
    - Depois do yield: executa ações de finalização (shutdown), se necessário.
    """

    setup_logging()
    yield
