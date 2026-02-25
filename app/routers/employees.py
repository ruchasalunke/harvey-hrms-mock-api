from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db_models import Employee as EmployeeModel
from app.models.schemas import Employee
from app.auth import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])


@router.get("", response_model=List[Employee])
def list_employees(
    department_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(EmployeeModel)
    if department_id:
        query = query.filter(EmployeeModel.department_id == department_id)
    if status:
        query = query.filter(EmployeeModel.status == status)
    if location:
        query = query.filter(EmployeeModel.location.ilike(f"%{location}%"))
    return query.all()


@router.get("/search/by-email", response_model=Employee)
def get_employee_by_email(email: str = Query(...), db: Session = Depends(get_db)):
    emp = db.query(EmployeeModel).filter(EmployeeModel.email.ilike(email)).first()
    if not emp:
        raise HTTPException(status_code=404, detail=f"No employee found with email '{email}'.")
    return emp


@router.get("/search/by-name", response_model=List[Employee])
def search_employees_by_name(name: str = Query(...), db: Session = Depends(get_db)):
    results = db.query(EmployeeModel).filter(
        EmployeeModel.first_name.ilike(f"%{name}%") |
        EmployeeModel.last_name.ilike(f"%{name}%")
    ).all()
    if not results:
        raise HTTPException(status_code=404, detail=f"No employees found matching '{name}'.")
    return results


@router.get("/{employee_id}", response_model=Employee)
def get_employee(employee_id: str, db: Session = Depends(get_db)):
    emp = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail=f"Employee '{employee_id}' not found.")
    return emp


@router.get("/{employee_id}/reports", response_model=List[Employee])
def get_direct_reports(employee_id: str, db: Session = Depends(get_db)):
    emp = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail=f"Employee '{employee_id}' not found.")
    return db.query(EmployeeModel).filter(EmployeeModel.manager_id == employee_id).all()