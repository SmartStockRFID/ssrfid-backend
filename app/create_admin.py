from app.database import SessionLocal
from app.models.usuario import Usuario
from app.crud.usuario import get_password_hash
from app.models.peca import Base as PecaBase
from app.models.usuario import Base as UsuarioBase
from app.database import engine

# Cria todas as tabelas dos modelos
PecaBase.metadata.create_all(bind=engine)
UsuarioBase.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")

def create_admin_user():
    db = SessionLocal()
    if not db.query(Usuario).filter(Usuario.username == "admin").first():
        admin = Usuario(
            username="admin",
            password_hash=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin)
        db.commit()
        print("Usuário admin criado com sucesso!")
    else:
        print("Usuário admin já existe.")
    db.close()

if __name__ == "__main__":
    create_admin_user()

# Para rodar este script, use o seguinte comando:
# python -m app.create_admin