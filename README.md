# Estoque Toyota Newland - Backend

Sistema de gerenciamento de estoque de peças Toyota, desenvolvido com FastAPI, SQLAlchemy e PostgreSQL. Inclui autenticação JWT, CRUD de peças e etiquetas, busca avançada, integração com interface Tkinter para testes locais e scripts de administração e migração de banco de dados.

## Principais Funcionalidades
- **API RESTful** com FastAPI
- **Banco de dados PostgreSQL** via SQLAlchemy
- **CRUD completo** para peças e etiquetas
- **Busca por nome** e por RFID UID
- **Autenticação JWT** (usuário e admin)
- **Criação automática do usuário admin** ao rodar o seed
- **Interface Tkinter** para testes locais
- **Scripts de migração** para atualização automática do banco sem perda de dados

## Estrutura de Pastas
```
app/
  ├── main.py            # Inicialização FastAPI
  ├── database.py        # Conexão e sessão com o banco
  ├── settings.py        # Configurações (POSTGRES_URL)
  ├── models/            # Modelos SQLAlchemy (peca, etiqueta, usuario)
  ├── schemas/           # Schemas Pydantic
  ├── crud/              # Funções CRUD
  ├── routers/           # Rotas FastAPI
  ├── auth.py            # Autenticação JWT
  ├── seed.py            # Popula peças, etiquetas e cria admin
  ├── create_admin.py    # Script manual para admin
  └── create_tables.py   # Criação e migração automática de tabelas

tk_estoque.py            # Interface Tkinter
```

## Configuração
1. **Crie o arquivo `.env` ou configure `app/settings.py`**
   - Defina a variável `POSTGRES_URL` com sua string de conexão PostgreSQL.

2. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Crie as tabelas e garanta a migração automática:**
   ```sh
   python -m app.create_tables
   ```

4. **Popule o banco e crie o admin:**
   ```sh
   python -m app.seed
   # Usuário admin: admin / admin123
   ```

5. **Inicie o servidor:**
   ```sh
   uvicorn app.main:app --reload
   ```

6. **(Opcional) Rode a interface Tkinter:**
   ```sh
   python tk_estoque.py
   ```

## Endpoints Principais
- `POST /login` — Autenticação JWT
- `GET /pecas/` — Listar peças
- `GET /pecas/busca?nome=...` — Buscar peças por nome
- `GET /pecas/{id}` — Buscar peça por ID
- `POST /pecas/` — Criar peça
- `PUT /pecas/{id}` — Atualizar peça
- `DELETE /pecas/{id}` — Deletar peça
- `GET /pecas/etiquetas/` — Listar etiquetas
- `GET /pecas/etiquetas/{id}` — Buscar etiqueta por ID
- `POST /pecas/etiquetas/` — Criar etiqueta
- `PUT /pecas/etiquetas/{id}` — Atualizar etiqueta
- `DELETE /pecas/etiquetas/{id}` — Deletar etiqueta
- `POST /usuarios/` — Criar usuário (apenas admin)

## Observações
- O usuário admin é criado automaticamente ao rodar o `seed.py`.
- O banco de dados deve estar acessível e configurado corretamente.
- O frontend pode ser integrado via CORS (origem padrão: `http://localhost:3000`).
- O script `create_tables.py` garante que a coluna `codigo_tipo` será adicionada automaticamente à tabela `pecas` sem perda de dados.
- O modelo de dados foi atualizado: agora há tabelas separadas para Peça e Etiqueta, com OEM/RFID em Etiqueta e referência de categoria em Peça.

---

Desenvolvido para controle de estoque Toyota Newland. Dúvidas? Abra uma issue ou entre em contato.
