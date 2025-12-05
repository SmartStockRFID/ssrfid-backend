from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_usuario_by_id(db: Session, id: str):
    return db.query(Usuario).filter(Usuario.id == id).first()


def get_usuario_by_username(db: Session, username: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.username == username).first()


def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(
        username=usuario.username, password_hash=get_password_hash(usuario.password), role=usuario.role
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def get_usuarios(db: Session) -> list[Usuario]:
    return db.query(Usuario).all()


def inativar_usuario(db: Session, usuario_id: int) -> Usuario | None:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        return None
    if not usuario.is_active:
        return usuario
    usuario.is_active = False
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
