from fastapi import APIRouter, HTTPException
from app import jobs, scheduler
from app.schema import JobRead, JobCreate
from uuid import UUID

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/jobs", response_model=list[JobRead],
            summary="List all jobs with default limit of 100",
            description="Returns all jobs with pagination support. Use `limit` and `offset` for large datasets.")
def list_jobs(limit: int = 100, offset: int = 0):
    rows = jobs.list_jobs(limit=limit, offset=offset)
    return rows

@router.get("/jobs/{job_id}", response_model=JobRead,
            tags=["Jobs"],
    summary="Create a new job",
    description="""
Create a new scheduled job.  

- **schedule_type**: `"cron"` or `"interval"`  
- **schedule_expr**:  
    - For `cron`: use standard cron expressions like `"*/5 * * * *"`  
    - For `interval`: use `key=value` pairs like `"seconds=30"`  
- **timezone**: Optional, defaults to `"UTC"`  
""",)
def get_job(job_id: UUID):
    job = jobs.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/jobs", response_model=JobRead, status_code=201)
def create_job(job_in: JobCreate):
    payload = job_in.model_dump()
    payload.update({"status": "enabled"})
    job = jobs.create_job(payload)
    scheduler.schedule_job(job)
    return job