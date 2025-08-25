from sqlalchemy.orm import Session

from app.models.peca import Peca
from app.schemas.peca import PecaCreate, PecaFilter, PecaUpdate


# Create
def create_peca(db: Session, peca: PecaCreate):
    db_peca = Peca(**peca.model_dump())
    db.add(db_peca)
    db.commit()
    db.refresh(db_peca)
    return db_peca


# Read all
def get_pecas(db: Session):
    return db.query(Peca).all()


# Read by id
def get_peca(db: Session, peca_id: int):
    return db.query(Peca).filter(Peca.id == peca_id).first()


# Update
def update_peca(db: Session, peca_id: int, peca: PecaUpdate):
    db_peca = db.query(Peca).filter(Peca.id == peca_id).first()
    if db_peca:
        for key, value in peca.dict(exclude_unset=True).items():
            setattr(db_peca, key, value)
        db.commit()
        db.refresh(db_peca)
    return db_peca


def listar_pecas_com_filtro(db: Session, filtros: PecaFilter) -> list[Peca]:
    query = db.query(Peca)

    if filtros.nome:
        query = query.filter(Peca.nome.ilike(f"%{filtros.nome}%"))

    if filtros.codigo_categoria:
        query = query.filter(Peca.codigo_categoria == filtros.codigo_categoria)

    return query.all()


# Delete
def delete_peca(db: Session, peca_id: int):
    db_peca = db.query(Peca).filter(Peca.id == peca_id).first()
    if db_peca:
        db.delete(db_peca)
        db.commit()
    return db_peca
