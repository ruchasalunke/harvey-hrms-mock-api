from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.data.mock_data import EMPLOYEES
from app.models.schemas import Employee

router = APIRouter()


@router.get("", response_model=List[Employee])
def list_employees(
    department_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
):
    results = EMPLOYEES
    if department_id:
        results = [e for e in results if e["department_id"] == department_id]
    if status:
        results = [e for e in results if e["status"] == status]
    if location:
        results = [e for e in results if location.lower() in e["location"].lower()]
    return results


@router.get("/search/by-email", response_model=Employee)
def get_employee_by_email(email: str = Query(...)):
    for emp in EMPLOYEES:
        if emp["email"].lower() == email.lower():
            return emp
    raise HTTPException(status_code=404, detail=f"No employee found with email '{email}'.")


@router.get("/search/by-name", response_model=List[Employee])
def search_employees_by_name(name: str = Query(...)):
    results = [
        e for e in EMPLOYEES
        if name.lower() in e["first_name"].lower() or name.lower() in e["last_name"].lower()
    ]
    if not results:
        raise HTTPException(status_code=404, detail=f"No employees found matching '{name}'.")
    return results


@router.get("/{employee_id}", response_model=Employee)
def get_employee(employee_id: str):
    for emp in EMPLOYEES:
        if emp["id"] == employee_id:
            return emp
    raise HTTPException(status_code=404, detail=f"Employee '{employee_id}' not found.")


@router.get("/{employee_id}/reports", response_model=List[Employee])
def get_direct_reports(employee_id: str):
    manager_ids = [e["id"] for e in EMPLOYEES]
    if employee_id not in manager_ids:
        raise HTTPException(status_code=404, detail=f"Employee '{employee_id}' not found.")
    return [e for e in EMPLOYEES if e.get("manager_id") == employee_id]