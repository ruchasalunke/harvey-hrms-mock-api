from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import uuid4
from app.database import get_db
from app.models.db_models import Interview as InterviewModel, Candidate as CandidateModel, Employee as EmployeeModel
from app.models.schemas import Interview, InterviewFeedbackUpdate, ScheduleInterviewRequest
from app.auth import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])


def _parse_interview(i: InterviewModel) -> dict:
    d = i.__dict__.copy()
    d["interviewers"] = d["interviewers"].split(",") if d["interviewers"] else []
    d["interviewer_names"] = d["interviewer_names"].split(",") if d["interviewer_names"] else []
    return d


@router.get("", response_model=List[Interview])
def list_interviews(
    candidate_id: Optional[str] = Query(None),
    job_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(InterviewModel)
    if candidate_id:
        query = query.filter(InterviewModel.candidate_id == candidate_id)
    if job_id:
        query = query.filter(InterviewModel.job_id == job_id)
    if status:
        query = query.filter(InterviewModel.status == status)
    return [_parse_interview(i) for i in query.all()]


@router.get("/{interview_id}", response_model=Interview)
def get_interview(interview_id: str, db: Session = Depends(get_db)):
    i = db.query(InterviewModel).filter(InterviewModel.id == interview_id).first()
    if not i:
        raise HTTPException(status_code=404, detail=f"Interview '{interview_id}' not found.")
    return _parse_interview(i)


@router.post("", response_model=Interview, status_code=201)
def schedule_interview(body: ScheduleInterviewRequest, db: Session = Depends(get_db)):
    candidate = db.query(CandidateModel).filter(CandidateModel.id == body.candidate_id).first()
    candidate_name = f"{candidate.first_name} {candidate.last_name}" if candidate else body.candidate_id

    id_to_name = {
        e.id: f"{e.first_name} {e.last_name}"
        for e in db.query(EmployeeModel).all()
    }
    interviewer_names = [id_to_name.get(eid, eid) for eid in body.interviewers]

    new_interview = InterviewModel(
        id=f"int-{str(uuid4())[:6]}",
        candidate_id=body.candidate_id,
        candidate_name=candidate_name,
        job_id=body.job_id,
        job_title=body.job_id,
        interview_type=body.interview_type,
        round=body.round,
        status="scheduled",
        scheduled_at=body.scheduled_at,
        duration_minutes=body.duration_minutes,
        interviewers=",".join(body.interviewers),
        interviewer_names=",".join(interviewer_names),
        location=body.location,
        meet_link=body.meet_link,
        feedback=None,
        score=None,
        notes=body.notes,
    )
    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)
    return _parse_interview(new_interview)


@router.patch("/{interview_id}/feedback", response_model=Interview)
def submit_feedback(interview_id: str, body: InterviewFeedbackUpdate, db: Session = Depends(get_db)):
    i = db.query(InterviewModel).filter(InterviewModel.id == interview_id).first()
    if not i:
        raise HTTPException(status_code=404, detail=f"Interview '{interview_id}' not found.")
    i.feedback = body.feedback
    i.score = body.score
    i.status = "completed"
    db.commit()
    db.refresh(i)
    return _parse_interview(i)


@router.patch("/{interview_id}/cancel", response_model=Interview)
def cancel_interview(interview_id: str, db: Session = Depends(get_db)):
    i = db.query(InterviewModel).filter(InterviewModel.id == interview_id).first()
    if not i:
        raise HTTPException(status_code=404, detail=f"Interview '{interview_id}' not found.")
    i.status = "cancelled"
    db.commit()
    db.refresh(i)
    return _parse_interview(i)