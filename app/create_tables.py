from app.models.peca import Base as PecaBase
from app.models.usuario import Base as UsuarioBase
from app.database import engine

# Cria todas as tabelas dos modelos (inclui Etiqueta, Peca e Usuario)
PecaBase.metadata.create_all(bind=engine)
UsuarioBase.metadata.create_all(bind=engine)

# Adiciona a coluna codigo_tipo à tabela pecas, se não existir
with engine.connect() as connection:
    try:
        connection.execute('ALTER TABLE pecas ADD COLUMN codigo_tipo INTEGER;')
        print("Coluna codigo_tipo adicionada à tabela pecas.")
    except Exception as e:
        if 'already exists' in str(e) or 'duplicate column' in str(e):
            print("Coluna codigo_tipo já existe.")
        else:
            print(f"Erro ao adicionar coluna: {e}")

print("Tabelas criadas e verificação da coluna codigo_tipo concluída!")
