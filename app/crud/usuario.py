from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_usuario_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()

def create_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(
        username=usuario.username,
        password_hash=get_password_hash(usuario.password),
        role=usuario.role
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario
