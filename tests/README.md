# Testes de Integração

Este diretório contém os testes de integração da aplicação ssrfid-backend.

## Estrutura

- `conftest.py`: Fixtures compartilhadas entre todos os testes
- `test_auth.py`: Testes de autenticação (login, tokens JWT)
- `test_usuario.py`: Testes de gerenciamento de usuários
- `test_peca.py`: Testes de CRUD de peças
- `test_conferencia.py`: Testes de conferência de estoque

## Executar os testes

### Com taskipy (recomendado)

```bash
# Executar todos os testes
task test

# Executar com cobertura
task test-cov
```

### Com pytest diretamente

```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/test_auth.py
pytest tests/test_usuario.py::TestUsuario::test_criar_usuario_como_admin

# Com verbosidade
pytest -v

# Com cobertura
pytest --cov=app --cov-report=html
```

## Fixtures Disponíveis

### Banco de Dados
- `db_session`: Sessão de banco de dados isolada (SQLite em memória)
- `client`: Cliente de teste FastAPI com banco isolado

### Usuários
- `admin_user`: Usuário com role admin
- `stockist_user`: Usuário com role stockist
- `admin_token`: Token JWT do admin
- `stockist_token`: Token JWT do stockist
- `admin_headers`: Headers HTTP com autenticação admin
- `stockist_headers`: Headers HTTP com autenticação stockist

### Dados de Teste
- `peca_data`: Dados de exemplo para criação de peça
- `peca_criada`: Peça já criada no banco
- `conferencia_criada`: Conferência ativa no banco

## Padrões de Teste

### Nomenclatura
- Classes: `TestNomeDoRecurso`
- Métodos: `test_acao_cenario`

### Estrutura de um teste
```python
def test_nome_do_teste(self, client, fixtures_necessarias):
    """Descrição clara do que o teste faz."""
    # Arrange: preparar dados
    dados = {"campo": "valor"}
    
    # Act: executar ação
    response = client.post("/endpoint", json=dados, headers=headers)
    
    # Assert: verificar resultado
    assert response.status_code == 200
    assert response.json()["campo"] == "valor"
```

## Cenários Testados

### Autenticação
- ✅ Login com credenciais válidas
- ✅ Login com credenciais inválidas
- ✅ Obtenção de usuário atual
- ✅ Validação de tokens

### Usuários
- ✅ Criação de usuário (admin only)
- ✅ Listagem de usuários (admin only)
- ✅ Inativação de usuário (admin only)
- ✅ Controle de acesso por role

### Peças
- ✅ CRUD completo (admin only)
- ✅ Listagem com filtros
- ✅ Validação de dados

### Conferências
- ✅ Iniciar conferência
- ✅ Registrar leituras RFID
- ✅ Registrar eventos
- ✅ Encerrar/Cancelar conferência
- ✅ Listar leituras e eventos
- ✅ Obter conferência ativa

## Dependências

```toml
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.28.1  # já incluído no projeto
```

## CI/CD

Os testes podem ser integrados ao pipeline CI/CD:

```yaml
# Exemplo para GitHub Actions
- name: Run tests
  run: |
    pip install pytest pytest-asyncio
    pytest -v
```

## Cobertura de Código

Após executar `task test-cov`, abra `htmlcov/index.html` no navegador para ver o relatório detalhado de cobertura.
