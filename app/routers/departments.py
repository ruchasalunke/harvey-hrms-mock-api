from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db_models import Department as DepartmentModel
from app.models.schemas import Department
from app.auth import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])


@router.get("", response_model=List[Department])
def list_departments(db: Session = Depends(get_db)):
    return db.query(DepartmentModel).all()


@router.get("/{department_id}", response_model=Department)
def get_department(department_id: str, db: Session = Depends(get_db)):
    d = db.query(DepartmentModel).filter(DepartmentModel.id == department_id).first()
    if not d:
        raise HTTPException(status_code=404, detail=f"Department '{department_id}' not found.")
    return d