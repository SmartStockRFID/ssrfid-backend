# Estoque API
# Estoque Toyota Newland - Backend

Sistema de gerenciamento de estoque de peças Toyota, desenvolvido com FastAPI, SQLAlchemy e PostgreSQL. Inclui autenticação JWT, CRUD de peças, busca avançada, e integração com interface Tkinter para testes locais.

## Principais Funcionalidades
- **API RESTful** com FastAPI
- **Banco de dados PostgreSQL** via SQLAlchemy
- **CRUD completo** para peças (modelos Toyota)
- **Busca por nome** e por RFID UID
- **Autenticação JWT** (usuário e admin)
- **Criação automática do usuário admin** ao rodar o seed
- **CORS configurado** para frontend
- **Interface Tkinter** para testes locais

## Estrutura de Pastas
```
app/
  ├── main.py            # Inicialização FastAPI
  ├── database.py        # Conexão e sessão com o banco
  ├── settings.py        # Configurações (POSTGRES_URL)
  ├── models/            # Modelos SQLAlchemy (peca, usuario)
  ├── schemas/           # Schemas Pydantic
  ├── crud/              # Funções CRUD
  ├── routers/           # Rotas FastAPI
  ├── auth.py            # Autenticação JWT
  ├── seed.py            # Popula peças e cria admin
  └── create_admin.py    # (opcional) Script manual para admin

   ou
```

## Configuração
1. **Crie o arquivo `.env` ou configure `app/settings.py`**
   - Defina a variável `POSTGRES_URL` com sua string de conexão PostgreSQL.

2. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Popule o banco e crie o admin:**
   ```sh
   python -m app.seed
   # Usuário admin: admin / admin123
   ```

4. **Inicie o servidor:**
   ```sh
   uvicorn app.main:app --reload
   ```

5. **(Opcional) Rode a interface Tkinter:**
   ```sh
   python tk_estoque.py
   ```

## Endpoints Principais
- `POST /login` — Autenticação JWT
- `GET /pecas/` — Listar peças
- `GET /pecas/busca?nome=...` — Buscar por nome
- `GET /pecas/search?rfid_uid=...` — Buscar por RFID
- `POST /pecas/` — Criar peça
- `PUT /pecas/{id}` — Atualizar peça
- `DELETE /pecas/{id}` — Deletar peça
- `POST /usuarios/` — Criar usuário (apenas admin)

## Observações
- O usuário admin é criado automaticamente ao rodar o `seed.py`.
- O banco de dados deve estar acessível e configurado corretamente.
- O frontend pode ser integrado via CORS (origem padrão: `http://localhost:3000`).

---

Desenvolvido para controle de estoque Toyota Newland. Dúvidas? Abra uma issue ou entre em contato.
   ```
   uvicorn app.main:app --reload
   ```

5. Acesse a documentação interativa:
   - [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints principais

- `GET /pecas` — Lista todas as peças
- `GET /pecas/{id}` — Busca peça por ID
- `GET /pecas/search?rfid_uid=` — Busca peça por RFID UID
- `POST /pecas` — Cria uma nova peça
- `PUT /pecas/{id}` — Atualiza uma peça
- `DELETE /pecas/{id}` — Remove uma peça

## Esquema da API

O esquema OpenAPI está disponível em [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json).

---

**Equipe:**  
Projeto colaborativo para controle de estoque automotivo.
