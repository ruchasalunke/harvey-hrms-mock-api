from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.data.mock_data import JOB_POSTINGS
from app.models.schemas import JobPosting

router = APIRouter()


@router.get("", response_model=List[JobPosting])
def list_jobs(
    status: Optional[str] = Query(None),
    department_id: Optional[str] = Query(None),
):
    results = JOB_POSTINGS
    if status:
        results = [j for j in results if j["status"] == status]
    if department_id:
        results = [j for j in results if j["department_id"] == department_id]
    return results


@router.get("/open", response_model=List[JobPosting])
def list_open_jobs():
    return [j for j in JOB_POSTINGS if j["status"] == "open"]


@router.get("/{job_id}", response_model=JobPosting)
def get_job(job_id: str):
    for job in JOB_POSTINGS:
        if job["id"] == job_id:
            return job
    raise HTTPException(status_code=404, detail=f"Job posting '{job_id}' not found.")