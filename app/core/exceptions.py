from fastapi import status


class AppException(Exception):
    def __init__(self, detail: str, code: int, log_msg: str | None = None):
        self.detail = detail
        self.code = code
        self.log_msg = log_msg or detail
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
