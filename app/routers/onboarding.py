import json
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db_models import Onboarding as OnboardingModel
from app.models.schemas import Onboarding
from app.auth import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])


def _parse_onboarding(o: OnboardingModel) -> dict:
    d = o.__dict__.copy()
    d["tasks"] = json.loads(d["tasks"]) if d["tasks"] else []
    return d


@router.get("", response_model=List[Onboarding])
def list_onboarding(status: Optional[str] = Query(None), db: Session = Depends(get_db)):
    query = db.query(OnboardingModel)
    if status:
        query = query.filter(OnboardingModel.status == status)
    return [_parse_onboarding(o) for o in query.all()]


@router.get("/employee/{employee_id}", response_model=Onboarding)
def get_onboarding_by_employee(employee_id: str, db: Session = Depends(get_db)):
    o = db.query(OnboardingModel).filter(OnboardingModel.employee_id == employee_id).first()
    if not o:
        raise HTTPException(status_code=404, detail=f"No onboarding record for employee '{employee_id}'.")
    return _parse_onboarding(o)


@router.get("/{onboarding_id}", response_model=Onboarding)
def get_onboarding(onboarding_id: str, db: Session = Depends(get_db)):
    o = db.query(OnboardingModel).filter(OnboardingModel.id == onboarding_id).first()
    if not o:
        raise HTTPException(status_code=404, detail=f"Onboarding record '{onboarding_id}' not found.")
    return _parse_onboarding(o)


@router.patch("/{onboarding_id}/task", response_model=Onboarding)
def complete_task(onboarding_id: str, task_name: str = Query(...), db: Session = Depends(get_db)):
    o = db.query(OnboardingModel).filter(OnboardingModel.id == onboarding_id).first()
    if not o:
        raise HTTPException(status_code=404, detail=f"Onboarding '{onboarding_id}' not found.")
    tasks = json.loads(o.tasks)
    for task in tasks:
        if task_name.lower() in task["task"].lower():
            task["status"] = "done"
    done_count = sum(1 for t in tasks if t["status"] == "done")
    o.tasks = json.dumps(tasks)
    o.completion_percentage = int((done_count / len(tasks)) * 100)
    if o.completion_percentage == 100:
        o.status = "completed"
    elif o.completion_percentage > 0:
        o.status = "in_progress"
    db.commit()
    db.refresh(o)
    return _parse_onboarding(o)