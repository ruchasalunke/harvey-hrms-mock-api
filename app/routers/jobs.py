from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db_models import JobPosting as JobModel
from app.models.schemas import JobPosting
from app.auth import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])


def _parse_job(job: JobModel) -> dict:
    d = job.__dict__.copy()
    d["requirements"] = d["requirements"].split(",") if d["requirements"] else []
    return d


@router.get("", response_model=List[JobPosting])
def list_jobs(
    status: Optional[str] = Query(None),
    department_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(JobModel)
    if status:
        query = query.filter(JobModel.status == status)
    if department_id:
        query = query.filter(JobModel.department_id == department_id)
    return [_parse_job(j) for j in query.all()]


@router.get("/open", response_model=List[JobPosting])
def list_open_jobs(db: Session = Depends(get_db)):
    return [_parse_job(j) for j in db.query(JobModel).filter(JobModel.status == "open").all()]


@router.get("/{job_id}", response_model=JobPosting)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job posting '{job_id}' not found.")
    return _parse_job(job)