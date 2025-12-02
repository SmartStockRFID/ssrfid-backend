from typing import Any, Dict

from fastapi import status


class AppException(Exception):
    def __init__(
        self,
        detail: str,
        code: int,
        log_msg: str | None = None,
        headers: Dict[str, Any] | None = None,
    ):
        self.detail = detail
        self.code = code
        self.log_msg = log_msg or detail
        self.headers = headers
        super().__init__(self.detail)


class ConferenciaAlreadyInitialized(AppException):
    def __init__(self):
        super().__init__(
            detail="Conferência já inicializada",
            log_msg="Conflito: existe uma conferência ativa, não é possível criar outra",
            code=status.HTTP_400_BAD_REQUEST,
        )


class ConferenciaNotFound(AppException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            detail=detail if detail else "Conferência não encontrada",
            code=status.HTTP_404_NOT_FOUND,
        )


class ConferenciaAlreadyClosed(AppException):
    def __init__(self):
        super().__init__(
            detail="Conferência já fechada/cancelada",
            code=status.HTTP_409_CONFLICT,
        )


class FuncionarioNotFound(AppException):
    def __init__(self):
        super().__init__(
            detail="Funcionário não encontrado",
            code=status.HTTP_404_NOT_FOUND,
        )


class PecaNotFound(AppException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            detail=detail if detail else "Produto não encontrada",
            code=status.HTTP_404_NOT_FOUND,
        )


class UserNotFound(AppException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            detail=detail if detail else "Usuário não encontrado",
            code=status.HTTP_403_FORBIDDEN,
        )


class UserAlreadyRegistered(AppException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            detail=detail if detail else "Usuário inválido",
            code=status.HTTP_,
        )


class UnauthorizedUser(AppException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            detail=detail if detail else "Usuário não tem permissão para acessar este recurso",
            code=status.HTTP_403_FORBIDDEN,
        )


class CredentialsException(AppException):
    def __init__(self):
        super().__init__(
            detail="Usuário com credenciais inválidas",
            code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
