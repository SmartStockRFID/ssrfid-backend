class TestAuth:
    """Testes de integração para endpoints de autenticação."""

    def test_login_success(self, client, admin_user):
        """Testa login com credenciais válidas."""
        response = client.post("/auth/login", data={"username": "admin_test", "password": "admin123"})

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "access_expire" in data
        assert "refresh_expire" in data
        assert data["token_type"] == "bearer"

        # Valida que as datas de expiração são strings ISO format
        from datetime import datetime

        datetime.fromisoformat(data["access_expire"].replace("Z", "+00:00"))
        datetime.fromisoformat(data["refresh_expire"].replace("Z", "+00:00"))

    def test_login_invalid_username(self, client):
        """Testa login com usuário inexistente."""
        response = client.post("/auth/login", data={"username": "usuario_inexistente", "password": "senha123"})

        assert response.status_code == 401
        assert response.json()["detail"] == "Usuário ou senha inválidos"

    def test_login_invalid_password(self, client, admin_user):
        """Testa login com senha incorreta."""
        response = client.post("/auth/login", data={"username": "admin_test", "password": "senha_errada"})

        assert response.status_code == 401
        assert response.json()["detail"] == "Usuário ou senha inválidos"

    def test_login_missing_fields(self, client):
        """Testa login sem fornecer todos os campos."""
        response = client.post("/auth/login", data={"username": "admin_test"})

        assert response.status_code == 422

    def test_get_current_user_with_valid_token(self, client, admin_headers, admin_user):
        """Testa obtenção do usuário atual com token válido."""
        response = client.get("/auth/me", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "admin_test"
        assert data["role"] == "admin"
        assert "id" in data

    def test_get_current_user_without_token(self, client):
        """Testa obtenção do usuário atual sem autenticação."""
        response = client.get("/auth/me")

        assert response.status_code == 401

    def test_get_current_user_with_invalid_token(self, client):
        """Testa obtenção do usuário atual com token inválido."""
        response = client.get("/auth/me", headers={"Authorization": "Bearer token_invalido"})

        assert response.status_code == 401

    def test_stockist_user_login(self, client, stockist_user):
        """Testa login de usuário stockist."""
        response = client.post("/auth/login", data={"username": "stockist_test", "password": "stockist123"})

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

        # Verifica se o token funciona
        me_response = client.get("/auth/me", headers={"Authorization": f"Bearer {data['access_token']}"})
        assert me_response.status_code == 200
        assert me_response.json()["role"] == "stockist"

    def test_login_returns_refresh_token(self, client, admin_user):
        """Testa que o login retorna access e refresh tokens com datas de expiração."""
        response = client.post("/auth/login", data={"username": "admin_test", "password": "admin123"})

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "access_expire" in data
        assert "refresh_expire" in data
        assert data["token_type"] == "bearer"

        # Valida formato ISO das datas
        from datetime import datetime

        access_exp = datetime.fromisoformat(data["access_expire"].replace("Z", "+00:00"))
        refresh_exp = datetime.fromisoformat(data["refresh_expire"].replace("Z", "+00:00"))

        # Refresh token deve expirar depois do access token
        assert refresh_exp > access_exp

    def test_refresh_token_success(self, client, admin_user):
        """Testa geração de novo access token com refresh token válido."""
        login_response = client.post("/auth/login", data={"username": "admin_test", "password": "admin123"})

        refresh_token = login_response.json()["refresh_token"]

        response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "access_expire" in data
        assert "refresh_expire" in data
        assert data["token_type"] == "bearer"

        # Valida formato das datas
        from datetime import datetime

        datetime.fromisoformat(data["access_expire"].replace("Z", "+00:00"))
        datetime.fromisoformat(data["refresh_expire"].replace("Z", "+00:00"))

        me_response = client.get("/auth/me", headers={"Authorization": f"Bearer {data['access_token']}"})
        assert me_response.status_code == 200
        assert me_response.json()["username"] == "admin_test"

    def test_refresh_token_invalid(self, client):
        """Testa refresh com token inválido."""
        response = client.post("/auth/refresh", json={"refresh_token": "token_invalido"})

        assert response.status_code == 401
        assert "inválido ou expirado" in response.json()["detail"].lower()

    def test_refresh_token_with_access_token(self, client, admin_token):
        """Testa que não é possível usar access token como refresh token."""
        response = client.post("/auth/refresh", json={"refresh_token": admin_token})

        assert response.status_code == 401

    def test_login_inactive_user(self, client, stockist_user, db_session):
        """Testa que usuário inativo não consegue fazer login."""
        stockist_user.is_active = False
        db_session.commit()

        response = client.post("/auth/login", data={"username": "stockist_test", "password": "stockist123"})

        assert response.status_code == 403
        assert "inativo" in response.json()["detail"].lower()

    def test_refresh_token_inactive_user(self, client, stockist_user, db_session):
        """Testa que usuário inativo não consegue fazer refresh."""
        login_response = client.post(
            "/auth/login", data={"username": "stockist_test", "password": "stockist123"}
        )
        refresh_token = login_response.json()["refresh_token"]

        stockist_user.is_active = False
        db_session.commit()

        response = client.post("/auth/refresh", json={"refresh_token": refresh_token})

        assert response.status_code == 403
        assert "inativo" in response.json()["detail"].lower()

    def test_token_expiration_times(self, client, admin_user):
        """Testa que os tempos de expiração estão corretos."""
        from datetime import datetime, timedelta, timezone

        before_login = datetime.now(timezone.utc)
        response = client.post("/auth/login", data={"username": "admin_test", "password": "admin123"})

        assert response.status_code == 200
        data = response.json()

        access_expire = datetime.fromisoformat(data["access_expire"].replace("Z", "+00:00"))
        refresh_expire = datetime.fromisoformat(data["refresh_expire"].replace("Z", "+00:00"))

        # Access token deve expirar em aproximadamente 60 minutos (1 hora)
        expected_access_expire = before_login + timedelta(minutes=60)
        access_diff = abs((access_expire - expected_access_expire).total_seconds())
        assert access_diff < 5, f"Access token expiration time off by {access_diff} seconds"

        # Refresh token deve expirar em aproximadamente 7 dias
        expected_refresh_expire = before_login + timedelta(days=7)
        refresh_diff = abs((refresh_expire - expected_refresh_expire).total_seconds())
        assert refresh_diff < 5, f"Refresh token expiration time off by {refresh_diff} seconds"

        # Refresh deve expirar depois do access
        assert refresh_expire > access_expire
