from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.data.mock_data import ONBOARDING
from app.models.schemas import Onboarding

router = APIRouter()

_onboarding = [dict(o) for o in ONBOARDING]


@router.get("", response_model=List[Onboarding])
def list_onboarding(status: Optional[str] = Query(None)):
    results = _onboarding
    if status:
        results = [o for o in results if o["status"] == status]
    return results


@router.get("/employee/{employee_id}", response_model=Onboarding)
def get_onboarding_by_employee(employee_id: str):
    for o in _onboarding:
        if o.get("employee_id") == employee_id:
            return o
    raise HTTPException(status_code=404, detail=f"No onboarding record for employee '{employee_id}'.")


@router.get("/{onboarding_id}", response_model=Onboarding)
def get_onboarding(onboarding_id: str):
    for o in _onboarding:
        if o["id"] == onboarding_id:
            return o
    raise HTTPException(status_code=404, detail=f"Onboarding record '{onboarding_id}' not found.")


@router.patch("/{onboarding_id}/task", response_model=Onboarding)
def complete_task(onboarding_id: str, task_name: str = Query(...)):
    for o in _onboarding:
        if o["id"] == onboarding_id:
            for task in o["tasks"]:
                if task_name.lower() in task["task"].lower():
                    task["status"] = "done"
            done_count = sum(1 for t in o["tasks"] if t["status"] == "done")
            o["completion_percentage"] = int((done_count / len(o["tasks"])) * 100)
            if o["completion_percentage"] == 100:
                o["status"] = "completed"
            elif o["completion_percentage"] > 0:
                o["status"] = "in_progress"
            return o
    raise HTTPException(status_code=404, detail=f"Onboarding '{onboarding_id}' not found.")