from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud.peca import create_peca, delete_peca, get_peca, listar_pecas_com_filtro, update_peca
from app.database import get_db
from app.schemas.auth import CurrentUser, AdminUser
from app.schemas.peca import PecaCreate, PecaFilter, PecaOut, PecaUpdate

router = APIRouter(
    prefix="/pecas",
    tags=["pecas"],
)


@router.get("", response_model=list[PecaOut])
def listar_pecas(user: CurrentUser, db: Session = Depends(get_db), filtros: PecaFilter = Query()):
    pecas = listar_pecas_com_filtro(db, filtros)
    return pecas


@router.get("/{peca_id}", response_model=PecaOut)
def buscar_peca(user: AdminUser, peca_id: int, db: Session = Depends(get_db)):
    peca = get_peca(db, peca_id)
    if not peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return peca


@router.post("", response_model=PecaOut)
def criar_peca(user: AdminUser, peca: PecaCreate, db: Session = Depends(get_db)):
    return create_peca(db, peca, created_by=user)


@router.put("/{peca_id}", response_model=PecaOut)
def atualizar_peca(user: AdminUser, peca_id: int, peca: PecaUpdate, db: Session = Depends(get_db)):
    db_peca = update_peca(db, peca_id, peca)
    if not db_peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return db_peca


@router.delete("/{peca_id}", response_model=PecaOut)
def deletar_peca(user: AdminUser, peca_id: int, db: Session = Depends(get_db)):
    db_peca = delete_peca(db, peca_id)
    if not db_peca:
        raise HTTPException(status_code=404, detail="Peça não encontrada")
    return db_peca
