from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import employees, jobs, candidates, interviews, departments, onboarding

app = FastAPI(
    title="Harvey Mock HRMS API",
    description="External mock HR system simulating Workday/BambooHR for Project Harvey integration testing.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router, prefix="/api/v1/employees", tags=["Employees"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Job Postings"])
app.include_router(candidates.router, prefix="/api/v1/candidates", tags=["Candidates"])
app.include_router(interviews.router, prefix="/api/v1/interviews", tags=["Interviews"])
app.include_router(departments.router, prefix="/api/v1/departments", tags=["Departments"])
app.include_router(onboarding.router, prefix="/api/v1/onboarding", tags=["Onboarding"])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "Harvey Mock HRMS API", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}