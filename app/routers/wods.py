from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.core.database import get_db
from app.models.wod import WOD
from app.schemas.wod import WODCreate, WODResponse

router = APIRouter(
    prefix="/wods",
    tags=["WODs (Entrenamientos)"]
)

@router.post("/", response_model=WODResponse, status_code=status.HTTP_201_CREATED)
def create_wod(wod: WODCreate, db: Session = Depends(get_db)):
    """Permite registrar un nuevo WOD en el sistema."""
    db_wod = WOD(**wod.dict())
    db.add(db_wod)
    db.commit()
    db.refresh(db_wod)
    return db_wod

@router.get("/", response_model=List[WODResponse])
def get_wods(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Lista todos los WODs registrados con paginación."""
    wods = db.query(WOD).offset(skip).limit(limit).all()
    return wods

@router.get("/fecha/{fecha_prog}", response_model=List[WODResponse])
def get_wod_by_date(fecha_prog: date, db: Session = Depends(get_db)):
    """Consulta los WODs programados para una fecha específica (YYYY-MM-DD)."""
    wods = db.query(WOD).filter(WOD.fecha_programada == fecha_prog).all()
    return wods