from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.peca import (
    get_pecas, get_peca, create_peca, update_peca, delete_peca, listar_pecas_com_filtro
)
from app.database import get_db
from app.schemas.peca import PecaOut, PecaCreate, PecaUpdate, PecaFilter
from app.models.peca import Peca

router = APIRouter(prefix="/pecas", tags=["pecas"])


@router.get("/", response_model=list[PecaOut])
def listar_pecas(db: Session = Depends(get_db), filtros: PecaFilter = Query()):
    pecas = listar_pecas_com_filtro(db, filtros)
    return pecas


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
