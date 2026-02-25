from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db_models import Candidate as CandidateModel
from app.models.schemas import Candidate, CandidateStatusUpdate
from app.auth import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])


def _parse_candidate(c: CandidateModel) -> dict:
    d = c.__dict__.copy()
    d["skills"] = d["skills"].split(",") if d["skills"] else []
    return d


@router.get("", response_model=List[Candidate])
def list_candidates(
    job_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    stage: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(CandidateModel)
    if job_id:
        query = query.filter(CandidateModel.job_id == job_id)
    if status:
        query = query.filter(CandidateModel.status == status)
    if stage:
        query = query.filter(CandidateModel.stage == stage)
    return [_parse_candidate(c) for c in query.all()]


@router.get("/search/by-email", response_model=Candidate)
def get_candidate_by_email(email: str = Query(...), db: Session = Depends(get_db)):
    c = db.query(CandidateModel).filter(CandidateModel.email.ilike(email)).first()
    if not c:
        raise HTTPException(status_code=404, detail=f"No candidate found with email '{email}'.")
    return _parse_candidate(c)


@router.get("/{candidate_id}", response_model=Candidate)
def get_candidate(candidate_id: str, db: Session = Depends(get_db)):
    c = db.query(CandidateModel).filter(CandidateModel.id == candidate_id).first()
    if not c:
        raise HTTPException(status_code=404, detail=f"Candidate '{candidate_id}' not found.")
    return _parse_candidate(c)


@router.patch("/{candidate_id}/status", response_model=Candidate)
def update_candidate_status(candidate_id: str, body: CandidateStatusUpdate, db: Session = Depends(get_db)):
    c = db.query(CandidateModel).filter(CandidateModel.id == candidate_id).first()
    if not c:
        raise HTTPException(status_code=404, detail=f"Candidate '{candidate_id}' not found.")
    c.status = body.status
    if body.notes:
        c.notes = (c.notes or "") + f"\n[Status update] {body.notes}"
    db.commit()
    db.refresh(c)
    return _parse_candidate(c)