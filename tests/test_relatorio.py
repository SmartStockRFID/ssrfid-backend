from datetime import datetime, timedelta

import pytest

from app.crud.conferencia import criar_conferencia
from app.schemas.conferencia import ConferenciaCreate


@pytest.fixture
def conferencia_finalizada(db_session, stockist_user):
    """Cria uma conferência finalizada para testes."""
    from app.models.conferencia import StatusConferencia

    conferencia_data = ConferenciaCreate(username_funcionario=stockist_user.username)
    conferencia = criar_conferencia(db_session, conferencia_data)

    # Simula finalização
    conferencia.status = StatusConferencia.FINALIZADA
    conferencia.finalizada_em = conferencia.iniciada_em + timedelta(minutes=30)
    db_session.commit()

    return conferencia


@pytest.fixture
def conferencias_multiplas_datas(db_session, stockist_user, admin_user):
    """Cria conferências em diferentes datas para testar filtros."""
    from app.models.conferencia import StatusConferencia

    conferencias = []
    base_date = datetime(2024, 1, 1, 10, 0, 0)

    # Conferência antiga (janeiro)
    conf1_data = ConferenciaCreate(username_funcionario=stockist_user.username)
    conf1 = criar_conferencia(db_session, conf1_data)
    conf1.iniciada_em = base_date
    conf1.finalizada_em = base_date + timedelta(minutes=20)
    conf1.status = StatusConferencia.FINALIZADA
    conferencias.append(conf1)

    # Conferência meio do período (fevereiro)
    conf2_data = ConferenciaCreate(username_funcionario=admin_user.username)
    conf2 = criar_conferencia(db_session, conf2_data)
    conf2.iniciada_em = base_date + timedelta(days=45)
    conf2.finalizada_em = base_date + timedelta(days=45, minutes=35)
    conf2.status = StatusConferencia.FINALIZADA
    conferencias.append(conf2)

    # Conferência recente (março)
    conf3_data = ConferenciaCreate(username_funcionario=stockist_user.username)
    conf3 = criar_conferencia(db_session, conf3_data)
    conf3.iniciada_em = base_date + timedelta(days=90)
    conf3.finalizada_em = base_date + timedelta(days=90, minutes=15)
    conf3.status = StatusConferencia.FINALIZADA
    conferencias.append(conf3)

    # Conferência cancelada (janeiro)
    conf4_data = ConferenciaCreate(username_funcionario=admin_user.username)
    conf4 = criar_conferencia(db_session, conf4_data)
    conf4.iniciada_em = base_date + timedelta(days=10)
    conf4.status = StatusConferencia.CANCELADA
    conferencias.append(conf4)

    db_session.commit()
    return conferencias


class TestRelatorio:
    """Testes de integração para endpoints de relatórios."""

    def test_obter_metricas(self, client, admin_headers, conferencia_finalizada):
        """Testa obtenção de métricas gerais."""
        response = client.get("/relatorios/metricas", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()

        # Valida estrutura
        assert "total_conferencias" in data
        assert "conferencias_finalizadas" in data
        assert "conferencias_canceladas" in data
        assert "conferencias_em_andamento" in data
        assert "tempo_medio_geral_minutos" in data
        assert "funcionarios_mais_rapidos" in data
        assert "metricas_por_funcionario" in data

        # Valida tipos
        assert isinstance(data["total_conferencias"], int)
        assert isinstance(data["tempo_medio_geral_minutos"], (int, float))
        assert isinstance(data["funcionarios_mais_rapidos"], list)
        assert isinstance(data["metricas_por_funcionario"], list)

        # Valida que há pelo menos uma conferência
        assert data["total_conferencias"] >= 1
        assert data["conferencias_finalizadas"] >= 1

    def test_obter_metricas_sem_autenticacao(self, client):
        """Testa que métricas requerem autenticação."""
        response = client.get("/relatorios/metricas")

        assert response.status_code == 401

    def test_metricas_por_funcionario(self, client, admin_headers, conferencia_finalizada):
        """Testa detalhamento de métricas por funcionário."""
        response = client.get("/relatorios/metricas", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()

        # Verifica métricas por funcionário
        assert len(data["metricas_por_funcionario"]) >= 1

        funcionario = data["metricas_por_funcionario"][0]
        assert "funcionario_id" in funcionario
        assert "funcionario_username" in funcionario
        assert "total_conferencias" in funcionario
        assert "tempo_medio_minutos" in funcionario
        assert "conferencias_finalizadas" in funcionario
        assert "conferencias_canceladas" in funcionario

    def test_funcionarios_mais_rapidos(self, client, admin_headers, conferencia_finalizada):
        """Testa ranking de funcionários mais rápidos."""
        response = client.get("/relatorios/metricas", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()

        # Verifica funcionários mais rápidos (top 5)
        rapidos = data["funcionarios_mais_rapidos"]
        assert isinstance(rapidos, list)
        assert len(rapidos) <= 5

        # Se houver funcionários, verifica ordenação (do mais rápido)
        if len(rapidos) > 1:
            for i in range(len(rapidos) - 1):
                assert rapidos[i]["tempo_medio_minutos"] <= rapidos[i + 1]["tempo_medio_minutos"]

    def test_gerar_pdf(self, client, admin_headers, conferencia_finalizada):
        """Testa geração de PDF."""
        response = client.get("/relatorios/pdf", headers=admin_headers)

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert "attachment" in response.headers["content-disposition"]
        assert "relatorio_inventarios.pdf" in response.headers["content-disposition"]

        # Verifica que o PDF tem conteúdo
        assert len(response.content) > 0

        # Verifica assinatura PDF
        assert response.content[:4] == b"%PDF"

    def test_gerar_pdf_sem_autenticacao(self, client):
        """Testa que PDF requer autenticação."""
        response = client.get("/relatorios/pdf")

        assert response.status_code == 401

    def test_metricas_com_multiplas_conferencias(
        self, client, admin_headers, db_session, stockist_user, admin_user
    ):
        """Testa métricas com múltiplas conferências de diferentes funcionários."""
        from datetime import timedelta

        from app.models.conferencia import StatusConferencia

        # Cria conferências para diferentes funcionários
        for user in [stockist_user, admin_user]:
            conf_data = ConferenciaCreate(username_funcionario=user.username)
            conf = criar_conferencia(db_session, conf_data)
            conf.status = StatusConferencia.FINALIZADA
            conf.finalizada_em = conf.iniciada_em + timedelta(minutes=45)
            db_session.commit()

        response = client.get("/relatorios/metricas", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()

        # Deve ter métricas para pelo menos 2 funcionários
        assert len(data["metricas_por_funcionario"]) >= 2
        assert data["total_conferencias"] >= 2

    def test_metricas_sem_conferencias(self, client, admin_headers, db_session):
        """Testa métricas quando não há conferências."""
        # Remove todas as conferências
        from app.models.conferencia import Conferencia

        db_session.query(Conferencia).delete()
        db_session.commit()

        response = client.get("/relatorios/metricas", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()

        assert data["total_conferencias"] == 0
        assert data["conferencias_finalizadas"] == 0
        assert data["tempo_medio_geral_minutos"] == 0.0
        assert len(data["metricas_por_funcionario"]) == 0
        assert len(data["funcionarios_mais_rapidos"]) == 0


class TestRelatorioFiltros:
    """Testes específicos para filtros de data nos endpoints de relatórios."""

    def test_filtro_data_inicio(self, client, admin_headers, conferencias_multiplas_datas):
        """Testa filtro por data de início."""
        # Filtra apenas conferências após 1º de fevereiro
        data_inicio = "2024-02-01T00:00:00"

        response = client.get(
            f"/relatorios/metricas?data_inicio={data_inicio}",
            headers=admin_headers,
        )

        assert response.status_code == 200
        data = response.json()

        # Deve retornar apenas as 2 conferências de fevereiro e março
        assert data["total_conferencias"] == 2
        assert data["conferencias_finalizadas"] == 2

    def test_filtro_data_fim(self, client, admin_headers, conferencias_multiplas_datas):
        """Testa filtro por data de fim."""
        # Filtra apenas conferências até 31 de janeiro
        data_fim = "2024-01-31T23:59:59"

        response = client.get(
            f"/relatorios/metricas?data_fim={data_fim}",
            headers=admin_headers,
        )

        assert response.status_code == 200
        data = response.json()

        # Deve retornar apenas as 2 conferências de janeiro (1 finalizada, 1 cancelada)
        assert data["total_conferencias"] == 2
        assert data["conferencias_finalizadas"] == 1
        assert data["conferencias_canceladas"] == 1

    def test_filtro_periodo_especifico(self, client, admin_headers, conferencias_multiplas_datas):
        """Testa filtro por período específico (data_inicio e data_fim)."""
        # Filtra apenas fevereiro
        data_inicio = "2024-02-01T00:00:00"
        data_fim = "2024-02-28T23:59:59"

        response = client.get(
            f"/relatorios/metricas?data_inicio={data_inicio}&data_fim={data_fim}",
            headers=admin_headers,
        )

        assert response.status_code == 200
        data = response.json()

        # Deve retornar apenas 1 conferência de fevereiro
        assert data["total_conferencias"] == 1
        assert data["conferencias_finalizadas"] == 1
        assert data["conferencias_canceladas"] == 0

    def test_filtro_sem_resultados(self, client, admin_headers, conferencias_multiplas_datas):
        """Testa filtro que não retorna resultados."""
        # Filtra período sem conferências
        data_inicio = "2025-01-01T00:00:00"
        data_fim = "2025-01-31T23:59:59"

        response = client.get(
            f"/relatorios/metricas?data_inicio={data_inicio}&data_fim={data_fim}",
            headers=admin_headers,
        )

        assert response.status_code == 200
        data = response.json()

        assert data["total_conferencias"] == 0
        assert data["conferencias_finalizadas"] == 0
        assert data["tempo_medio_geral_minutos"] == 0.0

    def test_filtro_tempo_medio_calculado_corretamente(
        self, client, admin_headers, conferencias_multiplas_datas
    ):
        """Testa se o tempo médio é calculado corretamente com filtros."""
        # Filtra apenas janeiro (20 minutos de duração)
        data_inicio = "2024-01-01T00:00:00"
        data_fim = "2024-01-31T23:59:59"

        response = client.get(
            f"/relatorios/metricas?data_inicio={data_inicio}&data_fim={data_fim}",
            headers=admin_headers,
        )

        assert response.status_code == 200
        data = response.json()

        # Tempo médio deve ser 20 minutos (apenas 1 conferência finalizada)
        assert data["tempo_medio_geral_minutos"] == 20.0

    def test_metricas_por_funcionario_respeitam_filtros(
        self, client, admin_headers, conferencias_multiplas_datas
    ):
        """Testa se métricas por funcionário respeitam os filtros de data."""
        # Filtra período onde apenas stockist_user tem conferências
        data_inicio = "2024-03-01T00:00:00"
        data_fim = "2024-03-31T23:59:59"

        response = client.get(
            f"/relatorios/metricas?data_inicio={data_inicio}&data_fim={data_fim}",
            headers=admin_headers,
        )

        assert response.status_code == 200
        data = response.json()

        # Deve ter apenas 1 funcionário com conferências nesse período
        assert len(data["metricas_por_funcionario"]) == 1
        assert data["metricas_por_funcionario"][0]["total_conferencias"] == 1

    def test_funcionarios_mais_rapidos_com_filtros(self, client, admin_headers, conferencias_multiplas_datas):
        """Testa se ranking de funcionários mais rápidos respeita filtros."""
        # Filtra apenas janeiro e fevereiro
        data_inicio = "2024-01-01T00:00:00"
        data_fim = "2024-02-28T23:59:59"

        response = client.get(
            f"/relatorios/metricas?data_inicio={data_inicio}&data_fim={data_fim}",
            headers=admin_headers,
        )

        assert response.status_code == 200
        data = response.json()

        # Verifica que há funcionários no ranking
        assert len(data["funcionarios_mais_rapidos"]) >= 1

        # Verifica ordenação (do mais rápido ao mais lento)
        if len(data["funcionarios_mais_rapidos"]) > 1:
            for i in range(len(data["funcionarios_mais_rapidos"]) - 1):
                assert (
                    data["funcionarios_mais_rapidos"][i]["tempo_medio_minutos"]
                    <= data["funcionarios_mais_rapidos"][i + 1]["tempo_medio_minutos"]
                )

    def test_formato_data_invalido(self, client, admin_headers):
        """Testa erro com formato de data inválido."""
        response = client.get(
            "/relatorios/metricas?data_inicio=invalid-date",
            headers=admin_headers,
        )

        # FastAPI/Pydantic deve retornar erro de validação
        assert response.status_code == 422

    def test_data_fim_antes_data_inicio(self, client, admin_headers, conferencias_multiplas_datas):
        """Testa comportamento quando data_fim é anterior a data_inicio."""
        data_inicio = "2024-03-01T00:00:00"
        data_fim = "2024-01-01T00:00:00"

        response = client.get(
            f"/relatorios/metricas?data_inicio={data_inicio}&data_fim={data_fim}",
            headers=admin_headers,
        )

        # Query deve retornar vazio (sem conferências no período invertido)
        assert response.status_code == 200
        data = response.json()
        assert data["total_conferencias"] == 0
