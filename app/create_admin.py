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

pecas_modelos = [
    ("Filtro de Óleo", "Corolla", 1001),
    ("Filtro de Ar", "Corolla", 1001),
    ("Pastilha de Freio Dianteira", "Corolla", 1004),
    ("Pastilha de Freio Traseira", "Corolla", 1004),
    ("Amortecedor Dianteiro", "Hilux", 1003),
    ("Amortecedor Traseiro", "Hilux", 1003),
    ("Bateria", "Yaris", 1005),
    ("Velas de Ignição", "Etios", 1005),
    ("Correia Dentada", "Hilux", 1001),
    ("Radiador", "Corolla Cross", 1006),
    ("Alternador", "Hilux", 1005),
    ("Motor de Partida", "Corolla", 1005),
    ("Disco de Freio Dianteiro", "Corolla Cross", 1004),
    ("Disco de Freio Traseiro", "Corolla Cross", 1004),
    ("Bomba de Combustível", "Etios", 1010),
    ("Sensor de Oxigênio", "Yaris", 1010),
    ("Injetor", "Corolla", 1010),
    ("Kit Embreagem", "Hilux", 1008),
    ("Parabrisa", "Yaris", 1006),
    ("Retrovisor", "Corolla Cross", 1007),
]