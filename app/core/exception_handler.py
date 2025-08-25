import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from h11 import Request
from pydantic import BaseModel

from app.core.exceptions import AppException

logger = logging.getLogger(__name__)


class ErrorResponse(BaseModel):
    detail: str


class ExceptionHandler:
    @staticmethod
    def app_exception_handler(request: Request, exc: AppException):
        """
        Este handler captura qualquer exceção que herde de AppException
        e a formata em uma resposta JSON, usando log_msg para o log
        e detail para o cliente.
        """
        logger.error(exc.log_msg)

        return JSONResponse(
            status_code=exc.code,
            content=ErrorResponse(detail=exc.detail).model_dump(),
        )

    @staticmethod
    def generic_exception_handler(request: Request, exc: Exception):
        """
        Handler genérico para capturar qualquer erro não esperado.
        """
        logger.exception(f"Erro inesperado na requisição: {request.url.path}")
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(detail="Ocorreu um erro interno inesperado no servidor.").model_dump(),
        )

    @staticmethod
    def handle(app: FastAPI):
        """
        Registra todos os manipuladores de exceção na aplicação FastAPI.
        """
        app.add_exception_handler(AppException, ExceptionHandler.app_exception_handler)
        app.add_exception_handler(Exception, ExceptionHandler.generic_exception_handler)
        return app
