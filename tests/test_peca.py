import pytest

from app.crud.peca import create_peca
from app.schemas.peca import PecaCreate


@pytest.fixture
def peca_data():
    """Dados de exemplo para criação de peça."""
    return {
        "nome": "Peça Teste",
        "codigo_produto": "PT001",
        "descricao": "Descrição da peça teste",
        "localizacao": "A1",
    }


@pytest.fixture
def peca_criada(db_session, peca_data, admin_user):
    """Cria uma peça no banco para testes."""
    peca = PecaCreate(**peca_data)
    return create_peca(db_session, peca, admin_user)


class TestPeca:
    """Testes de integração para endpoints de peças."""

    def test_criar_peca_como_stockist(self, client, stockist_headers, peca_data):
        """Testa que stockist não pode criar peças."""
        response = client.post("/pecas/", json=peca_data, headers=stockist_headers)

        assert response.status_code == 403

    def test_criar_peca_sem_autenticacao(self, client, peca_data):
        """Testa criação de peça sem autenticação."""
        response = client.post("/pecas/", json=peca_data)

        assert response.status_code == 401

    def test_listar_pecas_como_admin(self, client, admin_headers, peca_criada):
        """Testa listagem de peças por administrador."""
        response = client.get("/pecas/", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(p["id"] == peca_criada.id for p in data)

    def test_listar_pecas_com_filtro_nome(self, client, admin_headers, peca_criada):
        """Testa listagem de peças com filtro de nome."""
        response = client.get("/pecas/", params={"nome": "Teste"}, headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all("teste" in p["nome"].lower() for p in data)

    def test_listar_pecas_com_filtro_sem_resultado(self, client, admin_headers):
        """Testa listagem de peças com filtro que não retorna resultados."""
        response = client.get("/pecas/", params={"nome": "PeçaInexistente123"}, headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    def test_buscar_peca_por_id(self, client, admin_headers, peca_criada):
        """Testa busca de peça específica por ID."""
        response = client.get(f"/pecas/{peca_criada.id}", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == peca_criada.id
        assert data["nome"] == peca_criada.nome

    def test_buscar_peca_inexistente(self, client, admin_headers):
        """Testa busca de peça que não existe."""
        response = client.get("/pecas/999999", headers=admin_headers)

        assert response.status_code == 404
        assert "não encontrada" in response.json()["detail"].lower()

    def test_atualizar_peca(self, client, admin_headers, peca_criada):
        """Testa atualização de peça."""
        dados_atualizacao = {
            "nome": "Peça Atualizada",
            "codigo_produto": "PT002",
            "descricao": "Nova descrição",
            "localizacao": "B2",
        }

        response = client.put(f"/pecas/{peca_criada.id}", json=dados_atualizacao, headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Peça Atualizada"
        assert data["codigo_produto"] == "PT002"
        assert data["localizacao"] == "B2"

    def test_atualizar_peca_inexistente(self, client, admin_headers, peca_data):
        """Testa atualização de peça que não existe."""
        response = client.put("/pecas/999999", json=peca_data, headers=admin_headers)

        assert response.status_code == 404

    def test_deletar_peca(self, client, admin_headers, peca_criada):
        """Testa deleção de peça."""
        peca_id = peca_criada.id

        response = client.delete(f"/pecas/{peca_id}", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == peca_id

        # Verifica que a peça foi deletada
        response_busca = client.get(f"/pecas/{peca_id}", headers=admin_headers)
        assert response_busca.status_code == 404

    def test_deletar_peca_inexistente(self, client, admin_headers):
        """Testa deleção de peça que não existe."""
        response = client.delete("/pecas/999999", headers=admin_headers)

        assert response.status_code == 404

    def test_criar_peca_com_dados_invalidos(self, client, admin_headers):
        """Testa criação de peça com dados inválidos."""
        response = client.post(
            "/pecas/",
            json={
                "nome": "",
                "codigo_produto": "",
            },
            headers=admin_headers,
        )

        assert response.status_code == 422

    def test_listar_pecas_como_stockist(self, client, stockist_headers):
        """Testa que stockist não pode listar peças."""
        response = client.get("/pecas/", headers=stockist_headers)

        assert response.status_code == 403
