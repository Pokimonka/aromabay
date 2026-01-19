from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import crud, schemas, models

router = APIRouter(prefix="/perfumes", tags=["perfumes"])

@router.get("/", response_model=List[schemas.PerfumeResponse])
def read_perfumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    perfumes = crud.get_perfumes(db, skip=skip, limit=limit)
    return perfumes

@router.get("/{perfume_id}", response_model=schemas.PerfumeResponse)
def read_perfume(perfume_id: int, db: Session = Depends(get_db)):
    perfume = crud.get_perfume(db, perfume_id=perfume_id)
    if perfume is None:
        raise HTTPException(status_code=404, detail="Perfume not found")
    return perfume

@router.post("/", response_model=schemas.PerfumeResponse)
def create_perfume(perfume: schemas.PerfumeCreate, db: Session = Depends(get_db)):
    print("create_perfume")
    return crud.create_perfume(db=db, perfume=perfume)


@router.delete("/{perfume_id}", response_model=schemas.PerfumeResponse)
def create_perfume(perfume_id:int, db: Session = Depends(get_db)):

    return crud.delete_perfume(db=db, perfume_id=perfume_id)