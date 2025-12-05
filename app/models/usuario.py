from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.schemas.usuario import RoleEnum


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    created_by_id = Column(ForeignKey("usuarios.id"))
    created_by = relationship(
        "Usuario", remote_side=[id], backref="created_users", foreign_keys=[created_by_id]
    )
    pecas_criadas = relationship("Peca", back_populates="usuario")
