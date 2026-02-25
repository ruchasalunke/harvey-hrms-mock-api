from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from uuid import uuid4
from app.data.mock_data import INTERVIEWS, CANDIDATES, EMPLOYEES
from app.models.schemas import Interview, InterviewFeedbackUpdate, ScheduleInterviewRequest

router = APIRouter()

_interviews = [dict(i) for i in INTERVIEWS]


def _resolve_names(employee_ids: List[str]) -> List[str]:
    id_to_name = {
        e["id"]: f"{e['first_name']} {e['last_name']}"
        for e in EMPLOYEES
    }
    return [id_to_name.get(eid, eid) for eid in employee_ids]


@router.get("", response_model=List[Interview])
def list_interviews(
    candidate_id: Optional[str] = Query(None),
    job_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    results = _interviews
    if candidate_id:
        results = [i for i in results if i["candidate_id"] == candidate_id]
    if job_id:
        results = [i for i in results if i["job_id"] == job_id]
    if status:
        results = [i for i in results if i["status"] == status]
    return results


@router.get("/{interview_id}", response_model=Interview)
def get_interview(interview_id: str):
    for i in _interviews:
        if i["id"] == interview_id:
            return i
    raise HTTPException(status_code=404, detail=f"Interview '{interview_id}' not found.")


@router.post("", response_model=Interview, status_code=201)
def schedule_interview(body: ScheduleInterviewRequest):
    candidate_name = body.candidate_id
    for c in CANDIDATES:
        if c["id"] == body.candidate_id:
            candidate_name = f"{c['first_name']} {c['last_name']}"
            break

    new_interview = {
        "id": f"int-{str(uuid4())[:6]}",
        "candidate_id": body.candidate_id,
        "candidate_name": candidate_name,
        "job_id": body.job_id,
        "job_title": body.job_id,
        "interview_type": body.interview_type,
        "round": body.round,
        "status": "scheduled",
        "scheduled_at": body.scheduled_at,
        "duration_minutes": body.duration_minutes,
        "interviewers": body.interviewers,
        "interviewer_names": _resolve_names(body.interviewers),
        "location": body.location,
        "meet_link": body.meet_link,
        "feedback": None,
        "score": None,
        "notes": body.notes,
    }
    _interviews.append(new_interview)
    return new_interview


@router.patch("/{interview_id}/feedback", response_model=Interview)
def submit_feedback(interview_id: str, body: InterviewFeedbackUpdate):
    for i in _interviews:
        if i["id"] == interview_id:
            i["feedback"] = body.feedback
            i["score"] = body.score
            i["status"] = "completed"
            return i
    raise HTTPException(status_code=404, detail=f"Interview '{interview_id}' not found.")


@router.patch("/{interview_id}/cancel", response_model=Interview)
def cancel_interview(interview_id: str):
    for i in _interviews:
        if i["id"] == interview_id:
            i["status"] = "cancelled"
            return i
    raise HTTPException(status_code=404, detail=f"Interview '{interview_id}' not found.")