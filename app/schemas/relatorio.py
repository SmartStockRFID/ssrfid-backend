from datetime import datetime

from pydantic import BaseModel, Field


class DashboardFilters(BaseModel):
    """Filtros para o dashboard de métricas."""

    data_inicio: datetime | None = Field(None)
    data_fim: datetime | None = Field(None)


class FuncionarioMetricas(BaseModel):
    """Métricas individuais de um funcionário."""

    funcionario_id: int
    funcionario_username: str
    total_conferencias: int
    tempo_medio_minutos: float
    conferencias_finalizadas: int
    conferencias_canceladas: int


class MetricasGerais(BaseModel):
    """Métricas gerais do sistema de inventário."""

    total_conferencias: int
    conferencias_finalizadas: int
    conferencias_canceladas: int
    conferencias_em_andamento: int
    tempo_medio_geral_minutos: float
    funcionarios_mais_rapidos: list[FuncionarioMetricas]
    metricas_por_funcionario: list[FuncionarioMetricas]


class ConferenciaRelatorio(BaseModel):
    """Dados de uma conferência para o relatório."""

    id: int
    funcionario_username: str
    status: str
    iniciada_em: datetime
    finalizada_em: datetime | None
    duracao_minutos: float | None
    total_leituras: int
    total_pecas: int

    class Config:
        from_attributes = True
