from io import BytesIO

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.crud.relatorio import get_conferencias_para_relatorio, get_metricas_gerais
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.relatorio import DashboardFilters, MetricasGerais

router = APIRouter(prefix="/relatorios", tags=["relatorios"])


@router.get("/metricas", response_model=MetricasGerais)
def obter_metricas(
    filters: DashboardFilters = Query(),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """
    Retorna métricas essenciais sobre inventários:
    - Tempo médio de inventário
    - Métricas por funcionário
    - Funcionários mais rápidos (top 5)
    """
    return get_metricas_gerais(db, filters)


@router.get("/pdf")
def gerar_relatorio_pdf(
    filters: DashboardFilters = Query(),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """
    Gera um PDF com relatório completo de todos os inventários em formato de tabela.
    """
    conferencias = get_conferencias_para_relatorio(db, filters)

    # Criar buffer em memória para o PDF
    buffer = BytesIO()

    # Criar documento PDF em landscape para caber mais colunas
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    elements = []

    # Estilos
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]

    # Título
    title = Paragraph("Relatório de Inventários RFID", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3 * inch))

    # Preparar dados da tabela
    data = [["ID", "Funcionário", "Status", "Início", "Fim", "Duração (min)", "Leituras", "Peças"]]

    for conf in conferencias:
        data.append(
            [
                str(conf.id),
                conf.funcionario_username,
                conf.status.upper(),
                conf.iniciada_em.strftime("%d/%m/%Y %H:%M"),
                conf.finalizada_em.strftime("%d/%m/%Y %H:%M") if conf.finalizada_em else "-",
                str(conf.duracao_minutos) if conf.duracao_minutos else "-",
                str(conf.total_leituras),
                str(conf.total_pecas),
            ]
        )

    # Criar tabela
    table = Table(
        data,
        colWidths=[
            0.5 * inch,  # ID
            1.5 * inch,  # Funcionário
            1 * inch,  # Status
            1.5 * inch,  # Início
            1.5 * inch,  # Fim
            1 * inch,  # Duração
            0.8 * inch,  # Leituras
            0.8 * inch,  # Peças
        ],
    )

    # Estilo da tabela
    table.setStyle(
        TableStyle(
            [
                # Cabeçalho
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                # Corpo
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]
        )
    )

    elements.append(table)

    # Adicionar estatísticas no final
    metricas = get_metricas_gerais(db, filters)
    elements.append(Spacer(1, 0.5 * inch))

    stats_text = f"""
    <b>Estatísticas Gerais:</b><br/>
    Total de Inventários: {metricas.total_conferencias}<br/>
    Finalizados: {metricas.conferencias_finalizadas}<br/>
    Cancelados: {metricas.conferencias_canceladas}<br/>
    Em Andamento: {metricas.conferencias_em_andamento}<br/>
    Tempo Médio: {metricas.tempo_medio_geral_minutos:.2f} minutos
    """
    stats = Paragraph(stats_text, styles["Normal"])
    elements.append(stats)

    # Construir PDF
    doc.build(elements)

    # Retornar como resposta de stream
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=relatorio_inventarios.pdf"},
    )
