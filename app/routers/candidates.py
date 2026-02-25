from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.data.mock_data import CANDIDATES
from app.models.schemas import Candidate, CandidateStatusUpdate

router = APIRouter()

_candidates = [dict(c) for c in CANDIDATES]


@router.get("", response_model=List[Candidate])
def list_candidates(
    job_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    stage: Optional[str] = Query(None),
):
    results = _candidates
    if job_id:
        results = [c for c in results if c["job_id"] == job_id]
    if status:
        results = [c for c in results if c["status"] == status]
    if stage:
        results = [c for c in results if c["stage"] == stage]
    return results


@router.get("/search/by-email", response_model=Candidate)
def get_candidate_by_email(email: str = Query(...)):
    for c in _candidates:
        if c["email"].lower() == email.lower():
            return c
    raise HTTPException(status_code=404, detail=f"No candidate found with email '{email}'.")


@router.get("/{candidate_id}", response_model=Candidate)
def get_candidate(candidate_id: str):
    for c in _candidates:
        if c["id"] == candidate_id:
            return c
    raise HTTPException(status_code=404, detail=f"Candidate '{candidate_id}' not found.")


@router.patch("/{candidate_id}/status", response_model=Candidate)
def update_candidate_status(candidate_id: str, body: CandidateStatusUpdate):
    for c in _candidates:
        if c["id"] == candidate_id:
            c["status"] = body.status
            if body.notes:
                c["notes"] = (c.get("notes") or "") + f"\n[Status update] {body.notes}"
            return c
    raise HTTPException(status_code=404, detail=f"Candidate '{candidate_id}' not found.")