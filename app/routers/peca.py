from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud.peca import create_peca, delete_peca, get_peca, get_pecas, update_peca
from app.database import get_db
from app.models.peca import Peca
from app.schemas.peca import PecaCreate, PecaOut, PecaUpdate

router = APIRouter(prefix="/pecas", tags=["pecas"])


@router.get("/", response_model=list[PecaOut])
def listar_pecas(db: Session = Depends(get_db)):
    return get_pecas(db)


@router.get("/busca", response_model=list[PecaOut])
def buscar_pecas_por_nome(nome: str = Query(..., min_length=3), db: Session = Depends(get_db)):
    query = db.query(Peca).filter(func.lower(Peca.nome).contains(nome.lower()))
    resultados = query.all()
    if not resultados:
        raise HTTPException(status_code=404, detail="Nenhuma peça encontrada")
    return resultados



@router.get("/search", response_model=PecaOut)
def buscar_peca_por_rfid(rfid_uid: str, db: Session = Depends(get_db)):
    peca = db.query(Peca).filter(Peca.rfid_uid == rfid_uid).first()
    if not peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return peca


@router.get("/{peca_id}", response_model=PecaOut)
def buscar_peca(peca_id: int, db: Session = Depends(get_db)):
    peca = get_peca(db, peca_id)
    if not peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return peca


@router.post("/", response_model=PecaOut)
def criar_peca(peca: PecaCreate, db: Session = Depends(get_db)):
    return create_peca(db, peca)


@router.put("/{peca_id}", response_model=PecaOut)
def atualizar_peca(peca_id: int, peca: PecaUpdate, db: Session = Depends(get_db)):
    db_peca = update_peca(db, peca_id, peca)
    if not db_peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return db_peca


@router.delete("/{peca_id}", response_model=PecaOut)
def deletar_peca(peca_id: int, db: Session = Depends(get_db)):
    db_peca = delete_peca(db, peca_id)
    if not db_peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return db_peca
