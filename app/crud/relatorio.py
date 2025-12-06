from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.conferencia import Conferencia, Leitura, StatusConferencia
from app.schemas.relatorio import ConferenciaRelatorio, DashboardFilters, FuncionarioMetricas, MetricasGerais


def calcular_duracao_minutos(iniciada_em: datetime, finalizada_em: datetime | None) -> float | None:
    """Calcula a duração em minutos entre duas datas."""
    if not finalizada_em:
        return None
    duracao = finalizada_em - iniciada_em
    return duracao.total_seconds() / 60


def get_metricas_gerais(db: Session, filters: DashboardFilters) -> MetricasGerais:
    """Retorna métricas gerais do sistema de inventário."""

    data_inicio = filters.data_inicio
    data_fim = filters.data_fim

    # Filtros de data para as queries
    conferencia_query = db.query(Conferencia)
    if data_inicio and data_fim:
        conferencia_query = conferencia_query.filter(Conferencia.iniciada_em.between(data_inicio, data_fim))
    elif data_inicio:
        conferencia_query = conferencia_query.filter(Conferencia.iniciada_em >= data_inicio)
    elif data_fim:
        conferencia_query = conferencia_query.filter(Conferencia.iniciada_em <= data_fim)

    # Estatísticas básicas
    total_conferencias = conferencia_query.count()
    finalizadas = conferencia_query.filter(Conferencia.status == StatusConferencia.FINALIZADA).count()
    canceladas = conferencia_query.filter(Conferencia.status == StatusConferencia.CANCELADA).count()
    em_andamento = conferencia_query.filter(Conferencia.status == StatusConferencia.INICIADA).count()

    # Tempo médio geral (apenas finalizadas)
    conferencias_finalizadas_query = conferencia_query.filter(
        Conferencia.status == StatusConferencia.FINALIZADA,
        Conferencia.finalizada_em.isnot(None),
    )
    conferencias_finalizadas = conferencias_finalizadas_query.all()

    tempo_medio_geral = 0.0
    if conferencias_finalizadas:
        duracoes = [calcular_duracao_minutos(c.iniciada_em, c.finalizada_em) for c in conferencias_finalizadas]
        tempo_medio_geral = sum(d for d in duracoes if d) / len(duracoes) if duracoes else 0.0

    # Métricas por funcionário
    funcionarios = (
        conferencia_query.with_entities(Conferencia.id_funcionario, func.count(Conferencia.id).label("total"))
        .group_by(Conferencia.id_funcionario)
        .all()
    )

    metricas_por_funcionario = []
    for func_id, _ in funcionarios:
        metricas_funcionario = get_metricas_funcionario(db, func_id, filters)
        metricas_por_funcionario.append(metricas_funcionario)

    # Top 5 funcionários mais rápidos
    funcionarios_rapidos = sorted(
        [m for m in metricas_por_funcionario if m.tempo_medio_minutos > 0], key=lambda x: x.tempo_medio_minutos
    )[:5]

    return MetricasGerais(
        total_conferencias=total_conferencias,
        conferencias_finalizadas=finalizadas,
        conferencias_canceladas=canceladas,
        conferencias_em_andamento=em_andamento,
        tempo_medio_geral_minutos=round(tempo_medio_geral, 2),
        funcionarios_mais_rapidos=funcionarios_rapidos,
        metricas_por_funcionario=metricas_por_funcionario,
    )


def get_metricas_funcionario(
    db: Session, funcionario_id: int, filters: DashboardFilters | None = None
) -> FuncionarioMetricas:
    """Retorna métricas de um funcionário específico."""
    from app.models.usuario import Usuario

    funcionario = db.query(Usuario).filter(Usuario.id == funcionario_id).first()

    # Aplicar filtros de data se fornecidos
    conferencias_query = db.query(Conferencia).filter(Conferencia.id_funcionario == funcionario_id)

    if filters:
        if filters.data_inicio and filters.data_fim:
            conferencias_query = conferencias_query.filter(
                Conferencia.iniciada_em.between(filters.data_inicio, filters.data_fim)
            )
        elif filters.data_inicio:
            conferencias_query = conferencias_query.filter(Conferencia.iniciada_em >= filters.data_inicio)
        elif filters.data_fim:
            conferencias_query = conferencias_query.filter(Conferencia.iniciada_em <= filters.data_fim)

    conferencias = conferencias_query.all()

    total = len(conferencias)
    finalizadas = len([c for c in conferencias if c.status == StatusConferencia.FINALIZADA])
    canceladas = len([c for c in conferencias if c.status == StatusConferencia.CANCELADA])

    # Tempo médio
    conferencias_finalizadas = [
        c for c in conferencias if c.status == StatusConferencia.FINALIZADA and c.finalizada_em
    ]

    tempo_medio = 0.0
    if conferencias_finalizadas:
        duracoes = [calcular_duracao_minutos(c.iniciada_em, c.finalizada_em) for c in conferencias_finalizadas]
        tempo_medio = sum(d for d in duracoes if d) / len(duracoes) if duracoes else 0.0

    return FuncionarioMetricas(
        funcionario_id=funcionario_id,
        funcionario_username=funcionario.username if funcionario else "Desconhecido",
        total_conferencias=total,
        tempo_medio_minutos=round(tempo_medio, 2),
        conferencias_finalizadas=finalizadas,
        conferencias_canceladas=canceladas,
    )


def get_conferencias_para_relatorio(
    db: Session, filters: DashboardFilters | None = None
) -> list[ConferenciaRelatorio]:
    """Retorna todas as conferências formatadas para relatório."""
    conferencias_query = db.query(Conferencia)

    # Aplicar filtros de data se fornecidos
    if filters:
        if filters.data_inicio and filters.data_fim:
            conferencias_query = conferencias_query.filter(
                Conferencia.iniciada_em.between(filters.data_inicio, filters.data_fim)
            )
        elif filters.data_inicio:
            conferencias_query = conferencias_query.filter(Conferencia.iniciada_em >= filters.data_inicio)
        elif filters.data_fim:
            conferencias_query = conferencias_query.filter(Conferencia.iniciada_em <= filters.data_fim)

    conferencias = conferencias_query.order_by(Conferencia.iniciada_em.desc()).all()

    relatorio = []
    for conf in conferencias:
        # Conta leituras únicas
        total_leituras = db.query(func.count(Leitura.id)).filter(Leitura.conferencia_id == conf.id).scalar()

        # Soma total de peças lidas
        total_pecas = (
            db.query(func.sum(Leitura.quantidade)).filter(Leitura.conferencia_id == conf.id).scalar() or 0
        )

        duracao = calcular_duracao_minutos(conf.iniciada_em, conf.finalizada_em)

        relatorio.append(
            ConferenciaRelatorio(
                id=conf.id,
                funcionario_username=conf.funcionario.username if conf.funcionario else "Desconhecido",
                status=conf.status.value,
                iniciada_em=conf.iniciada_em,
                finalizada_em=conf.finalizada_em,
                duracao_minutos=round(duracao, 2) if duracao else None,
                total_leituras=total_leituras,
                total_pecas=total_pecas,
            )
        )

    return relatorio
