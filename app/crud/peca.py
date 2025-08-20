from sqlalchemy.orm import Session
from app.models.peca import Peca, Etiqueta
from app.schemas.peca import PecaCreate, PecaUpdate, EtiquetaCreate

# CRUD Peça
def create_peca(db: Session, peca: PecaCreate):
    db_peca = Peca(**peca.model_dump())
    db.add(db_peca)
    db.commit()
    db.refresh(db_peca)
    return db_peca

def get_pecas(db: Session):
    return db.query(Peca).all()

def get_peca(db: Session, peca_id: int):
    return db.query(Peca).filter(Peca.id == peca_id).first()

def update_peca(db: Session, peca_id: int, peca: PecaUpdate):
    db_peca = db.query(Peca).filter(Peca.id == peca_id).first()
    if db_peca:
        for key, value in peca.dict(exclude_unset=True).items():
            setattr(db_peca, key, value)
        db.commit()
        db.refresh(db_peca)
    return db_peca

def delete_peca(db: Session, peca_id: int):
    db_peca = db.query(Peca).filter(Peca.id == peca_id).first()
    if db_peca:
        db.delete(db_peca)
        db.commit()
    return db_peca

# CRUD Etiqueta
def create_etiqueta(db: Session, etiqueta: EtiquetaCreate):
    db_etiqueta = Etiqueta(**etiqueta.model_dump())
    db.add(db_etiqueta)
    db.commit()
    db.refresh(db_etiqueta)
    return db_etiqueta

def get_etiquetas(db: Session):
    return db.query(Etiqueta).all()

def get_etiqueta(db: Session, etiqueta_id: int):
    return db.query(Etiqueta).filter(Etiqueta.id == etiqueta_id).first()

def update_etiqueta(db: Session, etiqueta_id: int, etiqueta: EtiquetaCreate):
    db_etiqueta = db.query(Etiqueta).filter(Etiqueta.id == etiqueta_id).first()
    if db_etiqueta:
        for key, value in etiqueta.dict(exclude_unset=True).items():
            setattr(db_etiqueta, key, value)
        db.commit()
        db.refresh(db_etiqueta)
    return db_etiqueta

def delete_etiqueta(db: Session, etiqueta_id: int):
    db_etiqueta = db.query(Etiqueta).filter(Etiqueta.id == etiqueta_id).first()
    if db_etiqueta:
        db.delete(db_etiqueta)
        db.commit()
    return db_etiqueta
