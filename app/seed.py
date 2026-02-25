import json
from app.database import engine, SessionLocal, Base
from app.models.db_models import Department, Employee, JobPosting, Candidate, Interview, Onboarding
from app.data.mock_data import DEPARTMENTS, EMPLOYEES, JOB_POSTINGS, CANDIDATES, INTERVIEWS, ONBOARDING


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Only seed if tables are empty
        if db.query(Department).count() > 0:
            print("Database already seeded, skipping...")
            return

        print("Seeding departments...")
        for d in DEPARTMENTS:
            db.add(Department(**d))

        print("Seeding employees...")
        for e in EMPLOYEES:
            db.add(Employee(**e))

        print("Seeding job postings...")
        for j in JOB_POSTINGS:
            j = dict(j)
            j["requirements"] = ",".join(j["requirements"])
            db.add(JobPosting(**j))

        print("Seeding candidates...")
        for c in CANDIDATES:
            c = dict(c)
            c["skills"] = ",".join(c["skills"])
            db.add(Candidate(**c))

        print("Seeding interviews...")
        for i in INTERVIEWS:
            i = dict(i)
            i["interviewers"] = ",".join(i["interviewers"])
            i["interviewer_names"] = ",".join(i["interviewer_names"])
            db.add(Interview(**i))

        print("Seeding onboarding...")
        for o in ONBOARDING:
            o = dict(o)
            o["tasks"] = json.dumps(o["tasks"])
            db.add(Onboarding(**o))

        db.commit()
        print("Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()