from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    head = Column(String, nullable=True)
    headcount = Column(Integer, default=0)

    employees = relationship("Employee", back_populates="department_rel")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    department_id = Column(String, ForeignKey("departments.id"))
    department = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    employment_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    manager_id = Column(String, nullable=True)
    location = Column(String, nullable=False)

    department_rel = relationship("Department", back_populates="employees")


class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    department_id = Column(String, ForeignKey("departments.id"))
    department = Column(String, nullable=False)
    location = Column(String, nullable=False)
    employment_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    posted_date = Column(String, nullable=False)
    closing_date = Column(String, nullable=False)
    salary_min = Column(Float, nullable=False)
    salary_max = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)  # stored as comma-separated
    hiring_manager_id = Column(String, nullable=False)
    applicants_count = Column(Integer, default=0)


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    job_id = Column(String, ForeignKey("job_postings.id"))
    job_title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    stage = Column(String, nullable=False)
    applied_date = Column(String, nullable=False)
    resume_url = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    skills = Column(Text, nullable=False)  # stored as comma-separated
    experience_years = Column(Integer, default=0)
    current_company = Column(String, nullable=True)
    expected_salary = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    recruiter_id = Column(String, nullable=False)


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(String, primary_key=True)
    candidate_id = Column(String, ForeignKey("candidates.id"))
    candidate_name = Column(String, nullable=False)
    job_id = Column(String, ForeignKey("job_postings.id"))
    job_title = Column(String, nullable=False)
    interview_type = Column(String, nullable=False)
    round = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    scheduled_at = Column(String, nullable=False)
    duration_minutes = Column(Integer, default=60)
    interviewers = Column(Text, nullable=False)       # comma-separated IDs
    interviewer_names = Column(Text, nullable=False)  # comma-separated names
    location = Column(String, nullable=False)
    meet_link = Column(String, nullable=True)
    feedback = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)


class Onboarding(Base):
    __tablename__ = "onboarding"

    id = Column(String, primary_key=True)
    employee_id = Column(String, nullable=True)
    employee_name = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    department = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    buddy_id = Column(String, nullable=True)
    buddy_name = Column(String, nullable=True)
    status = Column(String, nullable=False)
    tasks = Column(Text, nullable=False)  # stored as JSON string
    completion_percentage = Column(Integer, default=0)
    notes = Column(Text, nullable=True)