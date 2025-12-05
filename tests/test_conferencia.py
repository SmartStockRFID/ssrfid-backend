from datetime import datetime

import pytest

from app.crud.conferencia import criar_conferencia
from app.crud.peca import create_peca
from app.schemas.conferencia import ConferenciaCreate, EventoCreate
from app.schemas.peca import PecaCreate


@pytest.fixture
def conferencia_criada(db_session, stockist_user):
    """Cria uma conferência ativa para testes."""
    conferencia_data = ConferenciaCreate(username_funcionario=stockist_user.username)
    return criar_conferencia(db_session, conferencia_data)


@pytest.fixture
def produto_criado(db_session, admin_user):
    """Cria um produto para testes."""
    produto_data = PecaCreate(
        nome="Produto Teste",
        codigo_produto="PT001",
        descricao="Descrição do produto teste",
        localizacao="A1",
    )
    return create_peca(db_session, produto_data, admin_user)


class TestConferencia:
    """Testes de integração para endpoints de conferência."""

    def test_iniciar_conferencia(self, client, admin_headers, stockist_user):
        """Testa início de nova conferência."""
        response = client.post(
            "/conferencia/", json={"username_funcionario": stockist_user.username}, headers=admin_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["status"] == "iniciada"

    def test_iniciar_conferencia_funcionario_inexistente(self, client, admin_headers):
        """Testa início de conferência com funcionário inexistente."""
        response = client.post(
            "/conferencia/", json={"username_funcionario": "funcionario_inexistente"}, headers=admin_headers
        )

        assert response.status_code == 404

    def test_iniciar_conferencia_ja_existe_ativa(
        self, client, admin_headers, conferencia_criada, stockist_user
    ):
        """Testa que não é possível iniciar nova conferência quando já existe uma ativa."""
        response = client.post(
            "/conferencia/", json={"username_funcionario": stockist_user.username}, headers=admin_headers
        )

        assert response.status_code == 409

    def test_listar_conferencias(self, client, admin_headers, conferencia_criada):
        """Testa listagem de conferências."""
        response = client.get("/conferencia/", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(c["id"] == conferencia_criada.id for c in data)

    def test_registrar_leitura_na_conferencia(self, client, admin_headers, conferencia_criada, produto_criado):
        """Testa registro de leituras RFID em conferência ativa."""

        leituras = [
            {
                "rfid_uuid": "RFID001",
                "codigo_produto": produto_criado.codigo_produto,
                "rfid_etiqueta": "ETIQ001",
                "lido_em": datetime.now().isoformat(),
            }
        ]

        response = client.post(
            f"/conferencia/{conferencia_criada.id}/leitura", json=leituras, headers=admin_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == conferencia_criada.id

    def test_registrar_leitura_conferencia_inexistente(self, client, admin_headers, produto_criado):
        """Testa registro de leitura em conferência inexistente."""
        leituras = [
            {
                "rfid_uuid": "RFID001",
                "codigo_produto": produto_criado.codigo_produto,
                "rfid_etiqueta": "ETIQ001",
                "lido_em": datetime.now().isoformat(),
            }
        ]

        response = client.post("/conferencia/999999/leitura", json=leituras, headers=admin_headers)

        assert response.status_code == 404

    def test_registrar_evento_na_conferencia(self, client, admin_headers, conferencia_criada):
        """Testa registro de eventos em conferência ativa."""

        eventos = [
            {"tipo": "PAUSA", "descricao": "Pausa para almoço", "ocorreu_em": datetime.now().isoformat()}
        ]

        response = client.post(
            f"/conferencia/{conferencia_criada.id}/evento", json=eventos, headers=admin_headers
        )

        assert response.status_code == 200

    def test_encerrar_conferencia(self, client, admin_headers, conferencia_criada, db_session):
        """Testa encerramento de conferência ativa."""
        response = client.put(f"/conferencia/{conferencia_criada.id}/encerrar", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "finalizada"

        # Verifica que não é possível encerrar novamente
        response_segunda = client.put(f"/conferencia/{conferencia_criada.id}/encerrar", headers=admin_headers)
        assert response_segunda.status_code == 409

    def test_cancelar_conferencia(self, client, admin_headers, conferencia_criada):
        """Testa cancelamento de conferência ativa."""
        response = client.put(f"/conferencia/{conferencia_criada.id}/cancelar", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "cancelada"

    def test_cancelar_conferencia_inexistente(self, client, admin_headers):
        """Testa cancelamento de conferência inexistente."""
        response = client.put("/conferencia/999999/cancelar", headers=admin_headers)

        assert response.status_code == 404

    def test_pegar_conferencia_ativa(self, client, conferencia_criada):
        """Testa endpoint para pegar conferência ativa."""
        response = client.get("/conferencia-ativa")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == conferencia_criada.id
        assert data["status"] == "iniciada"

    def test_pegar_conferencia_ativa_sem_conferencia(self, client):
        """Testa endpoint quando não há conferência ativa."""
        response = client.get("/conferencia-ativa")

        assert response.status_code == 204

    def test_listar_leituras_de_conferencia(self, client, admin_headers, conferencia_criada):
        """Testa listagem de leituras de uma conferência."""
        response = client.get(
            f"/conferencia/{conferencia_criada.id}/leituras",
            params={"limit": 10, "offset": 0},
            headers=admin_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "count" in data
        assert isinstance(data["items"], list)

    def test_listar_eventos_de_conferencia(self, client, admin_headers, conferencia_criada):
        """Testa listagem de eventos de uma conferência."""
        response = client.get(
            f"/conferencia/{conferencia_criada.id}/eventos",
            params={"limit": 10, "offset": 0},
            headers=admin_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "count" in data

    def test_registrar_leitura_conferencia_finalizada(
        self, client, admin_headers, conferencia_criada, db_session, produto_criado
    ):
        """Testa que não é possível registrar leitura em conferência finalizada."""
        # Primeiro encerra a conferência
        client.put(f"/conferencia/{conferencia_criada.id}/encerrar", headers=admin_headers)

        # Tenta registrar leitura
        leituras = [
            {
                "rfid_uuid": "RFID001",
                "codigo_produto": produto_criado.codigo_produto,
                "rfid_etiqueta": "ETIQ001",
                "lido_em": datetime.now().isoformat(),
            }
        ]

        response = client.post(
            f"/conferencia/{conferencia_criada.id}/leitura", json=leituras, headers=admin_headers
        )

        assert response.status_code == 409

    def test_iniciar_conferencia_sem_autenticacao(self, client, stockist_user):
        """Testa que não é possível iniciar conferência sem autenticação."""
        response = client.post("/conferencia/", json={"username_funcionario": stockist_user.username})

        assert response.status_code == 401
