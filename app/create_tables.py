from app.database import engine
from app.models.peca import Base as PecaBase
from app.models.usuario import Base as UsuarioBase

# Cria todas as tabelas dos modelos
PecaBase.metadata.create_all(bind=engine)
UsuarioBase.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")
