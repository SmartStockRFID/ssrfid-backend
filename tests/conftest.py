import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth import create_access_token
from app.crud.usuario import create_usuario
from app.database import get_db
from app.main import app
from app.models.base import Base
from app.schemas.usuario import RoleEnum, UsuarioCreate

# Cria banco de dados SQLite em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Cria uma nova sessão de banco de dados para cada teste."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Cria um cliente de teste com banco de dados isolado."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def admin_user(db_session):
    """Cria um usuário administrador para testes."""
    usuario = UsuarioCreate(username="admin_test", password="admin123", role=RoleEnum.admin)
    return create_usuario(db_session, usuario)


@pytest.fixture(scope="function")
def stockist_user(db_session):
    """Cria um usuário stockist para testes."""
    usuario = UsuarioCreate(username="stockist_test", password="stockist123", role=RoleEnum.stockist)
    return create_usuario(db_session, usuario)


@pytest.fixture(scope="function")
def admin_token(admin_user):
    """Gera token JWT para usuário administrador."""
    token, _ = create_access_token(data={"sub": admin_user.username, "role": admin_user.role})
    return token


@pytest.fixture(scope="function")
def stockist_token(stockist_user):
    """Gera token JWT para usuário stockist."""
    token, _ = create_access_token(data={"sub": stockist_user.username, "role": stockist_user.role})
    return token


@pytest.fixture(scope="function")
def admin_headers(admin_token):
    """Headers HTTP com autenticação de administrador."""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture(scope="function")
def stockist_headers(stockist_token):
    """Headers HTTP com autenticação de stockist."""
    return {"Authorization": f"Bearer {stockist_token}"}
