from fastapi import APIRouter, HTTPException
from typing import List
from app.data.mock_data import DEPARTMENTS
from app.models.schemas import Department

router = APIRouter()


@router.get("", response_model=List[Department])
def list_departments():
    return DEPARTMENTS


@router.get("/{department_id}", response_model=Department)
def get_department(department_id: str):
    for d in DEPARTMENTS:
        if d["id"] == department_id:
            return d
    raise HTTPException(status_code=404, detail=f"Department '{department_id}' not found.")