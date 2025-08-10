# Estoque API

API para gerenciamento de peças de estoque automotivo, desenvolvida em Python com FastAPI e PostgreSQL.

## Estrutura do Projeto

```
app/
  ├── crud/
  │     └── peca.py
  ├── models/
  │     └── peca.py
  ├── routers/
  │     └── peca.py
  ├── schemas/
  │     └── peca.py
  ├── database.py
  ├── main.py
  └── seed.py
venv/
run_server.bat
```

## Como rodar

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

2. Configure o banco de dados PostgreSQL e ajuste a variável `DATABASE_URL` em `app/database.py` se necessário.

3. Crie e popule o banco:
   ```
   python -m app.seed
   ```

4. Inicie o servidor:
   ```
   run_server.bat
   ```
   ou
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
