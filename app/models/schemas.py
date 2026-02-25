from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class EmploymentType(str, Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    intern = "intern"


class EmployeeStatus(str, Enum):
    active = "active"
    on_leave = "on_leave"
    terminated = "terminated"


class JobStatus(str, Enum):
    open = "open"
    closed = "closed"
    on_hold = "on_hold"


class CandidateStatus(str, Enum):
    applied = "applied"
    under_review = "under_review"
    interview_scheduled = "interview_scheduled"
    offer_extended = "offer_extended"
    offer_accepted = "offer_accepted"
    rejected = "rejected"
    withdrawn = "withdrawn"


class InterviewStatus(str, Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"
    rescheduled = "rescheduled"


class OnboardingStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class Employee(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    department_id: str
    department: str
    job_title: str
    employment_type: EmploymentType
    status: EmployeeStatus
    start_date: str
    salary: float
    currency: str
    manager_id: Optional[str]
    location: str


class JobPosting(BaseModel):
    id: str
    title: str
    department_id: str
    department: str
    location: str
    employment_type: EmploymentType
    status: JobStatus
    posted_date: str
    closing_date: str
    salary_min: float
    salary_max: float
    currency: str
    description: str
    requirements: List[str]
    hiring_manager_id: str
    applicants_count: int


class Candidate(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    job_id: str
    job_title: str
    status: CandidateStatus
    stage: str
    applied_date: str
    resume_url: Optional[str]
    linkedin: Optional[str]
    skills: List[str]
    experience_years: int
    current_company: Optional[str]
    expected_salary: Optional[float]
    notes: Optional[str]
    recruiter_id: str


class Interview(BaseModel):
    id: str
    candidate_id: str
    candidate_name: str
    job_id: str
    job_title: str
    interview_type: str
    round: int
    status: InterviewStatus
    scheduled_at: str
    duration_minutes: int
    interviewers: List[str]
    interviewer_names: List[str]
    location: str
    meet_link: Optional[str]
    feedback: Optional[str]
    score: Optional[float]
    notes: Optional[str]


class OnboardingTask(BaseModel):
    task: str
    status: str


class Onboarding(BaseModel):
    id: str
    employee_id: Optional[str]
    employee_name: str
    job_title: str
    department: str
    start_date: str
    buddy_id: Optional[str]
    buddy_name: Optional[str]
    status: OnboardingStatus
    tasks: List[OnboardingTask]
    completion_percentage: int
    notes: Optional[str]


class Department(BaseModel):
    id: str
    name: str
    head: Optional[str]
    headcount: int


class InterviewFeedbackUpdate(BaseModel):
    feedback: str
    score: float


class CandidateStatusUpdate(BaseModel):
    status: CandidateStatus
    notes: Optional[str] = None


class ScheduleInterviewRequest(BaseModel):
    candidate_id: str
    job_id: str
    interview_type: str
    round: int
    scheduled_at: str
    duration_minutes: int = 60
    interviewers: List[str]
    location: str = "Google Meet"
    meet_link: Optional[str] = None
    notes: Optional[str] = None