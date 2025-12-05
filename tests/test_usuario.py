class TestUsuario:
    """Testes de integração para endpoints de usuário."""

    def test_criar_usuario_como_admin(self, client, admin_headers):
        """Testa criação de novo usuário por administrador."""
        response = client.post(
            "/usuarios/",
            json={"username": "novo_usuario", "password": "senha123", "role": "stockist"},
            headers=admin_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "novo_usuario"
        assert data["role"] == "stockist"
        assert "id" in data

    def test_criar_usuario_duplicado(self, client, admin_headers, admin_user):
        """Testa criação de usuário com username já existente."""
        response = client.post(
            "/usuarios/",
            json={"username": "admin_test", "password": "senha123", "role": "admin"},
            headers=admin_headers,
        )

        assert response.status_code == 400

    def test_criar_usuario_sem_autenticacao(self, client):
        """Testa criação de usuário sem autenticação."""
        response = client.post(
            "/usuarios/", json={"username": "novo_usuario", "password": "senha123", "role": "stockist"}
        )

        assert response.status_code == 401

    def test_criar_usuario_como_stockist(self, client, stockist_headers):
        """Testa que stockist não pode criar usuários."""
        response = client.post(
            "/usuarios/",
            json={"username": "novo_usuario", "password": "senha123", "role": "stockist"},
            headers=stockist_headers,
        )

        assert response.status_code == 403

    def test_listar_usuarios_como_admin(self, client, admin_headers, admin_user, stockist_user):
        """Testa listagem de usuários por administrador."""
        response = client.get("/usuarios/", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2
        usernames = [u["username"] for u in data]
        assert "admin_test" in usernames
        assert "stockist_test" in usernames

    def test_listar_usuarios_como_stockist(self, client, stockist_headers):
        """Testa que stockist não pode listar usuários."""
        response = client.get("/usuarios/", headers=stockist_headers)

        assert response.status_code == 403

    def test_listar_usuarios_sem_autenticacao(self, client):
        """Testa listagem de usuários sem autenticação."""
        response = client.get("/usuarios/")

        assert response.status_code == 401

    def test_inativar_usuario_como_admin(self, client, admin_headers, stockist_user, db_session):
        """Testa inativação de usuário por administrador."""
        usuario_id = stockist_user.id

        response = client.put(f"/usuarios/{usuario_id}/inativar", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == usuario_id

        # Verifica que o usuário foi realmente inativado no banco
        db_session.refresh(stockist_user)
        assert stockist_user.is_active is False

    def test_inativar_usuario_como_stockist(self, client, stockist_headers, admin_user):
        """Testa que stockist não pode inativar usuários."""
        response = client.put(f"/usuarios/{admin_user.id}/inativar", headers=stockist_headers)

        assert response.status_code == 403

    def test_inativar_usuario_ja_inativo(self, client, admin_headers, stockist_user, db_session):
        """Testa inativação de usuário já inativo (idempotência)."""
        usuario_id = stockist_user.id

        # Primeira inativação
        client.put(f"/usuarios/{usuario_id}/inativar", headers=admin_headers)

        # Segunda inativação (deve ser idempotente)
        response = client.put(f"/usuarios/{usuario_id}/inativar", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == usuario_id

    def test_criar_usuario_com_dados_invalidos(self, client, admin_headers):
        """Testa criação de usuário com dados inválidos."""
        response = client.post(
            "/usuarios/",
            json={"username": "", "password": "123", "role": "invalid_role"},
            headers=admin_headers,
        )

        assert response.status_code == 422
